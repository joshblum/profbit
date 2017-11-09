from coinbase.wallet.client import OAuthClient

def _percent(investment, investment_return):
    if investment == 0:
        percent_return = 0
    else:
        percent_return = investment_return / investment
    return percent_return * 100


def get_coinbase_stats(access_token):
    client = OAuthClient(access_token, access_token)
    accounts = client.get_accounts()
    total_investment_return = 0
    total_investment = 0
    stats = {}
    for account in accounts.data:
        if account['type'] != 'wallet':
            # TODO(joshblum): Look into other wallet types
            continue
        currency = account['currency']
        total_balance = float(account['native_balance']['amount'])
        account_id = account['id']
        txs = client.get_transactions(account_id)
        investment = sum(float(tx['native_amount']['amount'])
                         for tx in txs.data
                         if tx['status'] == 'completed')
        investment_return = total_balance - investment
        percent_return = _percent(investment, investment_return)
        stats[currency] = {
            'name': currency,
            'investment': investment,
            'investment_return': investment_return,
            'percent_return': percent_return,
        }
        total_investment_return += investment_return
        total_investment += investment
    total_percent_return = _percent(
        total_investment, total_investment_return)
    stats = sorted(stats.values(), key=lambda x: x['name'])
    stats.insert(0, {
        'name': 'Total',
        'investment': total_investment,
        'investment_return': total_investment_return,
        'percent_return': total_percent_return,
    })
    return stats
