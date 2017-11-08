from social_core.backends.coinbase import CoinbaseOAuth2 as _CoinbaseOAuth2


class CoinbaseOAuth2(_CoinbaseOAuth2):
    # TODO(joshblum) Remove when fix is accepted in library
    # https://github.com/python-social-auth/social-core/pull/153

    def get_user_id(self, details, response):
        return response['data']['id']

    def get_user_details(self, response):
        """Return user details from Coinbase account"""
        user_data = response['data']
        email = user_data.get('email', '')
        name = user_data['name']
        username = user_data.get('username')
        fullname, first_name, last_name = self.get_user_names(name)
        return {'username': username,
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name,
                'email': email}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        return self.get_json(
            'https://api.coinbase.com/v2/user',
            headers={'Authorization': 'Bearer ' + access_token}
        )
