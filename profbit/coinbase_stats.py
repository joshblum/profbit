from copy import copy
from enum import Enum

from coinbase.wallet.client import OAuthClient
from dateutil.parser import parse

from .currency_map import CURRENCY_MAP


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


def _get_investment_data(client, account, period, stat_txs):
    """
    Get historic price data for the given `period` and `account`'s `currency`.
    We calculate how much our investment gained or lost at each historic
    data-point. We also calculate total stats for the period.
    """
    historic_prices = reversed(client.get_historic_prices(
        currency_pair=_get_currency_pair(account.currency.code,
                                         account.native_balance.currency),
        period=period,
    ).prices)

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
        date_time = parse(price_data.time)
        # Find first tx that is after this `price_data`
        while next_stat_tx and date_time >= next_stat_tx.date_time:
            curr_stat_tx = next_stat_tx
            curr_index += 1
            next_stat_tx = _next_tx(curr_index)
        if date_time < initial_stat_tx.date_time:
            roi = 0
        else:
            roi = _get_roi_from_price_data(curr_stat_tx, price_data)

        if period_begin_stat_tx is None and period_begin_price_data is None:
            if roi == 0:
                period_begin_stat_tx = StatTx(price_data.time, 0, 0)
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


def _get_stat_txs(client, account):
    """
    Gather all transactions for the given `account` from Coinbase.  Calculate
    the cumulative sum across the ordered transactions
    """
    coinbase_txs = client.get_transactions(account.id, order='asc')
    stat_txs = []
    for i, coinbase_tx in enumerate(coinbase_txs.data):
        if coinbase_tx.status != 'completed':
            continue
        stat_tx = StatTx(
            date_time=parse(coinbase_tx.created_at),
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


def get_coinbase_stats(access_token):
    """
    Get historical investment data across all accounts.
    """
    client = OAuthClient(access_token, access_token)
    user = client.get_current_user()
    accounts = client.get_accounts()
    stats = {}
    for account in accounts.data:
        if account.type != 'wallet':
            # TODO(joshblum): Look into other account types
            continue
        stat_txs = _get_stat_txs(client, account)
        investment_data = {}
        for stat_period in StatPeriod:
            period = stat_period.value
            investment_data[period] = _get_investment_data(
                client, account, period, stat_txs)
        currency_code = account.currency.code
        stats[currency_code] = investment_data
    native_currency = user.native_currency
    return {
        'stats': stats,
        'native_currency': native_currency,
        'native_currency_symbol': CURRENCY_MAP.get(native_currency, '$'),
    }
