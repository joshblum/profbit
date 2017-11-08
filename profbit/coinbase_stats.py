import locale

from coinbase.wallet.client import OAuthClient

locale.setlocale(locale.LC_ALL, '')


def _format_currency(amt):
    return locale.currency(amt, grouping=True)


def _format_percent(investment, investment_progress):
    if investment == 0:
        percent_return = 0
    else:
        percent_return = investment_progress / investment
    return '{:.2%}'.format(percent_return)


def get_coinbase_stats(access_token):
    client = OAuthClient(access_token, access_token)
    accounts = client.get_accounts()
    total_investment_progress = 0
    total_investment = 0
    stats = {}
    for account in accounts.data:
        currency = account['currency']
        total_balance = float(account['native_balance']['amount'])
        account_id = account['id']
        txs = client.get_transactions(account_id)
        investment = sum(float(tx['native_amount']['amount'])
                         for tx in txs.data
                         if tx['status'] == 'completed')
        investment_progress = total_balance - investment
        percent_return = _format_percent(investment, investment_progress)
        stats[currency] = {
            'investment': _format_currency(investment),
            'investment_progress': _format_currency(investment_progress),
            'percent_return': percent_return,
        }
        total_investment_progress += investment_progress
        total_investment += investment
    total_percent_return = _format_percent(
        total_investment, total_investment_progress)
    stats['total'] = {
        'investment': _format_currency(total_investment),
        'investment_progress': _format_currency(total_investment_progress),
        'percent_return': total_percent_return
    }
    return stats
