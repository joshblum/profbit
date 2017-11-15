from enum import Enum
from itertools import zip_longest

from coinbase.wallet.client import OAuthClient
from dateutil.parser import parse

class StatTx():

    def __init__(self, date_time=None, currency_amount=0, native_amount=0):
        self.date_time = date_time
        self.currency_amount = currency_amount
        self.native_amount = native_amount

    def __add__(self, other):
        # If we don't have a `date_time`, take it from `other`
        self.date_time = self.date_time or other.date_time
        self.currency_amount += other.currency_amount
        self.native_amount += other.native_amount
        return self

class StatPeriod(Enum):
    ALL = 'all'
    YEAR = 'year'
    MONTH = 'month'
    WEEK = 'week'
    DAY = 'day'
    HOUR = 'hour'

def _get_currency_pair(crypto, native):
    return '{}-{}'.format(crypto, native)

def _percent(investment, return_investment):
    if investment == 0:
        return_percent = 0
    else:
        return_percent = return_investment / investment
    return return_percent * 100

def _get_historic_investment_data(client, account, period, stat_txs):
    historic_price_data = client.get_historic_prices(
        currency_pair=_get_currency_pair(account.currency.code, account.native_balance.currency),
        period=period
    )
    historic_investment_data = []

    def _next_tx(index):
        index += 1
        if index >= len(stat_txs):
            return None
        return stat_txs[index]

    curr_index = 0
    curr_stat_tx = stat_txs[curr_index]
    next_stat_tx = _next_tx(curr_index)
    for price_data in historic_price_data.prices:
        date_time = parse(price_data.time)
        if next_stat_tx and date_time >= next_stat_tx.date_time:
            curr_stat_tx = next_stat_tx
            next_stat_tx = _next_tx(curr_index)
        if date_time < curr_stat_tx.date_time:
            price_data.price = 0.
        else:
            # Calculate how much of the given currency we had in the native
            # currency to compute the ROI.
            price_data.price = (float(price_data.price) * curr_stat_tx.currency_amount) - curr_stat_tx.native_amount

        price_data = dict(price_data)
        price_data['x'] = int(parse(price_data.pop('time')).strftime('%s'))
        price_data['y'] = price_data.pop('price')
        historic_investment_data.append(dict(price_data))
    return historic_investment_data

def _get_tx_data(client, account):
    """
    Calculates the total ROI for the given `account` in addition to the historic
    progress.
    """
    coinbase_txs = client.get_transactions(account.id)
    stat_txs = []
    for i, coinbase_tx in enumerate(coinbase_txs.data):
        if coinbase_tx.status != 'completed':
            continue
        stat_tx = StatTx(
                date_time=parse(coinbase_tx.created_at),
                    currency_amount=float(coinbase_tx.amount.amount),
                    native_amount=float(coinbase_tx.native_amount.amount))
        if i != 0:
            # Keep a running sum of our total to compare to historical data
            stat_tx += stat_txs[i-1]
        stat_txs.append(stat_tx)
    if not stat_tx:
        return {
            'investment': 0.,
            'historic_investment_data': {}
        }

    historic_investment_data = {}
    for stat_period in StatPeriod:
        if stat_period != StatPeriod.MONTH:
            continue
        period = stat_period.value
        historic_investment_data[period] = _get_historic_investment_data(client, account, period, stat_txs)

    return {
        'investment': stat_txs[-1].native_amount,
        'historic_investment_data': historic_investment_data,
    }


def get_coinbase_stats(access_token):
    """
    Gather all of the transaction data across all accounts
    """
    client = OAuthClient(access_token, access_token, api_version='2017-05-19')
    user = client.get_current_user()
    accounts = client.get_accounts()
    total_historic_investment_data = None
    total_return_investment = 0
    total_investment = 0
    stats = {}
    for account in accounts.data:
        if account.type != 'wallet':
            # TODO(joshblum): Look into other account types
            continue
        total_balance = float(account.native_balance.amount)
        account_id = account.id
        transaction_data = _get_tx_data(client, account)
        investment = transaction_data['investment']
        historic_investment_data = transaction_data['historic_investment_data']
        return_investment = total_balance - investment
        return_percent = _percent(investment, return_investment)
        currency_code = account.currency.code
        stats[currency_code] = {
            'name': currency_code,
            'investment': investment,
            'historic_investment_data': historic_investment_data,
            'return_investment': return_investment,
            'return_percent': return_percent,
            'native_currency': user.native_currency,
        }
        total_return_investment += return_investment
        total_investment += investment
    total_return_percent = _percent(
        total_investment, total_return_investment)
    stats = sorted(stats.values(), key=lambda x: x['name'])
    stats.insert(0, {
        'name': 'Total',
        'investment': total_investment,
        'return_investment': total_return_investment,
        'return_percent': total_return_percent,
        'native_currency': user.native_currency,
        'historic_investment_data': {},
    })
    return stats
