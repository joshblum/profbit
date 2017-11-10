from coinbase.wallet.client import OAuthClient


def _percent(investment, return_investment):
    if investment == 0:
        return_percent = 0
    else:
        return_percent = return_investment / investment
    return return_percent * 100


def get_coinbase_stats(access_token):
    client = OAuthClient(access_token, access_token)
    user = client.get_current_user()
    accounts = client.get_accounts()
    total_return_investment = 0
    total_investment = 0
    stats = {}
    for account in accounts.data:
        if account.type != 'wallet':
            # TODO(joshblum): Look into other wallet types
            continue
        currency = account.currency
        total_balance = float(account.native_balance.amount)
        account_id = account.id
        txs = client.get_transactions(account_id)
        investment = sum(float(tx.native_amount.amount)
                         for tx in txs.data
                         if tx.status == 'completed')
        return_investment = total_balance - investment
        return_percent = _percent(investment, return_investment)
        stats[currency] = {
            'name': currency,
            'investment': investment,
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
    })
    return stats
