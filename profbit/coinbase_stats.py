import datetime
import re
from collections import defaultdict
from copy import copy
from enum import Enum
from functools import lru_cache
from urllib import parse

from coinbase.wallet.client import OAuthClient

from .currency_map import CURRENCY_MAP

TIMESTAMP_REGEX = re.compile(
    r'(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})')


class StatTx():
    """
    Store information about a Coinbase transaction to compute against
    historical data.
    """

    def __init__(self, date_time, currency_amount=0, currency_code='',
                 native_amount=0, native_currency_code=''):
        self.date_time = date_time
        self.currency_amount = currency_amount
        self.currency_code = currency_code
        self.native_amount = native_amount
        self.native_currency_code = native_currency_code

    def __add__(self, other):
        self.currency_amount += other.currency_amount
        self.native_amount += other.native_amount
        return self

    def __sub__(self, other):
        self.currency_amount -= other.currency_amount
        self.native_amount -= other.native_amount
        return self

    def __repr__(self):
        return ('<StatTx> {self.native_currency_code}{self.native_amount} '
                '| {self.currency_code}{self.currency_amount} '
                '@ {self.date_time}').format(self=self)


class StatPeriod(Enum):
    """
    Periods which we can historical day for.
    """
    ALL = 'all'
    YEAR = 'year'
    MONTH = 'month'
    WEEK = 'week'
    DAY = 'day'
    HOUR = 'hour'


def parse_datetime(date_time):
    # https://stackoverflow.com/a/14163523/1213319
    return datetime.datetime(
            *map(int, TIMESTAMP_REGEX.match(date_time).groups()))


def paginate_response(client, func_name, *args, **kwargs):
    """
    Exhaust the available pages of data from the Coinbase client.
    """
    coinbase_func = getattr(client, func_name)
    coinbase_response = coinbase_func(*args, **kwargs)
    coinbase_data = coinbase_response.data
    while coinbase_response.pagination.next_uri:
        starting_after = parse.parse_qs(
                coinbase_response.pagination.next_uri).get('starting_after')
        kwargs['starting_after'] = starting_after

        coinbase_response = coinbase_func(*args, **kwargs)
        coinbase_data.extend(coinbase_response.data)
    return coinbase_data


def _get_currency_pair(currency, native):
    """
    Format a crypto currency with a native one for the Coinbase API.
    """
    return '{}-{}'.format(currency, native)


def _percent(investment, return_investment):
    if investment == 0:
        return_percent = 0
    else:
        return_percent = return_investment / investment
    return return_percent * 100


def _get_investment_data(client, currency_pair, period, stat_txs):
    """
    Get historic price data for the given `period` and `account`'s `currency`.
    We calculate how much our investment gained or lost at each historic
    data-point. We also calculate total stats for the period.
    """
    historic_prices = reversed(client.get_historic_prices(
        currency_pair=currency_pair,
        period=period,
    ).prices)
    stat_txs = stat_txs or [
        StatTx(datetime.datetime.now(), currency_amount=0, native_amount=0)
    ]

    def _next_tx(index):
        if index >= len(stat_txs):
            return None
        return stat_txs[index]

    def _get_roi_from_price_data(stat_tx, price_data):
        return ((float(price_data.price) * stat_tx.currency_amount) -
                stat_tx.native_amount)

    period_begin_stat_tx = None
    period_begin_price_data = None
    period_end_stat_tx = copy(stat_txs[-1])
    period_end_price_data = None

    curr_index = 0
    # Our first tx, any price data before this is irrelevant.
    initial_stat_tx = stat_txs[curr_index]
    curr_stat_tx = stat_txs[curr_index]
    curr_index += 1
    next_stat_tx = _next_tx(curr_index)
    historic_investment_data = []

    for price_data in historic_prices:
        date_time = parse_datetime(price_data.time)
        # Find first tx that is after this `price_data`
        while next_stat_tx and date_time >= next_stat_tx.date_time:
            curr_stat_tx = next_stat_tx
            curr_index += 1
            next_stat_tx = _next_tx(curr_index)
        if date_time < initial_stat_tx.date_time:
            # Remove long tail of 0s for the 'all' period.
            if period == 'all':
                continue
            roi = 0
        else:
            roi = _get_roi_from_price_data(curr_stat_tx, price_data)

        if period_begin_stat_tx is None and period_begin_price_data is None:
            if roi == 0:
                period_begin_stat_tx = StatTx(
                    price_data.time, currency_amount=0, native_amount=0)
            else:
                period_begin_stat_tx = copy(curr_stat_tx)
            period_begin_price_data = price_data

        historic_investment_data.append({
            'x': int(date_time.strftime('%s')),
            'y': roi,
        })

        # Get the final datapoint in the iterator.
        period_end_price_data = price_data

    period_begin_roi = _get_roi_from_price_data(
        period_begin_stat_tx, period_begin_price_data)
    period_end_roi = _get_roi_from_price_data(
        period_end_stat_tx, period_end_price_data)
    return_investment = period_end_roi - period_begin_roi
    return_percent = _percent(
        period_end_stat_tx.native_amount, return_investment)
    total_investment = (period_end_stat_tx -
                        period_begin_stat_tx).native_amount
    return {
        'period_investment_data': {
            'total_investment': total_investment,
            'return_investment': return_investment,
            'return_percent': return_percent,
        },
        'historic_investment_data': historic_investment_data,
    }


def _merge_stat_txs(array1, array2):
    left_idx = 0
    right_idx = 0
    merged = []
    while left_idx < len(array1) and right_idx < len(array2):
        left = array1[left_idx]
        right = array2[right_idx]
        if left.date_time < right.date_time:
            merged.append(left)
        else:
            merged.append(right)
    merged.extend(array1[left_idx:])
    merged.extend(array2[right_idx:])
    return merged


def _get_stat_txs(client, accounts):
    """
    Gather all transactions for the given `account` from Coinbase.  Calculate
    the cumulative sum across the ordered transactions
    """
    all_account_data = []
    # Create a sorted list of all transactions for a given currency
    for account in accounts:
        account_data = paginate_response(
            client, 'get_transactions',
            *(account.id,), **{'order': 'asc', 'limit': '100'})
        all_account_data = _merge_stat_txs(all_account_data, account_data)

    stat_txs = []

    for i, coinbase_tx in enumerate(all_account_data):
        if coinbase_tx.status != 'completed':
            continue
        stat_tx = StatTx(
            date_time=parse_datetime(coinbase_tx.created_at),
            currency_amount=float(coinbase_tx.amount.amount),
            currency_code=account.currency.code,
            native_amount=float(coinbase_tx.native_amount.amount),
            native_currency_code=account.native_balance.currency,
        )
        if i != 0:
            # Keep a running sum of our total to compare to historical data.
            stat_tx += stat_txs[i - 1]
        stat_txs.append(stat_tx)
    return stat_txs


def _get_stats_data_for_period(client, accounts, period):
    accounts = list(accounts)
    stat_txs = _get_stat_txs(client, accounts)
    account = accounts[0]
    currency_pair = _get_currency_pair(account.currency.code,
                                       account.native_balance.currency)
    return {
        period: _get_investment_data(client, currency_pair, period, stat_txs)
    }


def _get_total_data(client, accounts):
    account_mapping = defaultdict(list)
    for account in accounts:
        account_mapping[account.currency.code.lower()].append(account)

    total_return_investment = 0
    total_investment = 0
    stats = {}
    for currency, accounts in account_mapping.items():
        total_balance = sum(float(account.native_balance.amount)
                            for account in accounts)
        stat_txs = _get_stat_txs(client, accounts)
        stat_txs = stat_txs or [
            StatTx(datetime.datetime.now(), currency_amount=0, native_amount=0)
        ]
        investment = stat_txs[-1].native_amount
        return_investment = total_balance - investment
        stats[currency] = {
            'total_investment': investment,
            'return_investment': return_investment,
            'return_percent': _percent(investment, return_investment)
        }
        total_investment += investment
        total_return_investment += return_investment
    stats['total'] = {
        'total_investment': total_investment,
        'return_investment': total_return_investment,
        'return_percent': _percent(total_investment, total_return_investment)
    }
    return stats


@lru_cache(maxsize=512)
def _get_user_and_accounts(access_token, cache_date):
    """
    We cache API calls for the Coinbase `User` object and account data,
    refreshing it once per day. We pass in `cache_date` which has the
    current date, forcing an API call if the date changes (and eventually
    evicting expired dates).
    """
    client = OAuthClient(access_token, access_token)
    user = client.get_current_user()
    accounts = paginate_response(client, 'get_accounts', **{'limit': '100'})
    return (user, accounts)


def get_coinbase_stats(access_token, currency, period):
    """
    Get historical investment data across all accounts.
    """
    client = OAuthClient(access_token, access_token)
    cache_date = datetime.datetime.date(datetime.datetime.now())
    user, accounts = _get_user_and_accounts(access_token, cache_date)

    # TODO(joshblum): Look into other account types.
    accounts = filter(lambda account: account.type == 'wallet', accounts)
    if currency == 'total':
        stats_data = _get_total_data(client, accounts)
    else:
        accounts = filter(
            lambda account: account.currency.code.lower() == currency,
            accounts)
        stats_data = _get_stats_data_for_period(client, accounts, period)

    return {
        'stats': {currency: stats_data},
        'native_currency': user.native_currency,
        'native_currency_symbol': CURRENCY_MAP.get(user.native_currency, '$'),
    }
