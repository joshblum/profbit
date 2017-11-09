import os

SECRET_KEY = os.environ.get('SECRET_KEY', '')
SOCIAL_AUTH_COINBASE_KEY = os.environ.get('SOCIAL_AUTH_COINBASE_KEY', '')
SOCIAL_AUTH_COINBASE_SECRET = os.environ.get('SOCIAL_AUTH_COINBASE_SECRET', '')
SECRET_KEY = os.environ.get('SOCIAL_AUTH_COINBASE_SECRET', '')
IS_HEROKU = os.environ.get('IS_HEROKU', False)
FLASK_DEBUG = not IS_HEROKU
SESSION_COOKIE_NAME = 'psa_session'
DATABASE_URL = os.environ.get('DATABASE_URL', '/tmp/profbit.db')
DEBUG_TB_INTERCEPT_REDIRECTS = False
SESSION_PROTECTION = 'strong'
SOCIAL_AUTH_COINBASE_GET_ALL_EXTRA_DATA = True
SOCIAL_AUTH_COINBASE_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_COINBASE_SCOPE = [
    'wallet:accounts:read', 'wallet:transactions:read']
SOCIAL_AUTH_COINBASE_AUTH_EXTRA_ARGUMENTS = {
        'account': 'all',
        'referral': '5943d0d36785cd04ad5c2d25',
        'layout': 'signup',
}
SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/stats/'
SOCIAL_AUTH_USER_MODEL = 'profbit.models.User'
SOCIAL_AUTH_STORAGE = 'social_flask_peewee.models.FlaskStorage'
SOCIAL_AUTH_AUTHENTICATION_BACKENDS = (
    'profbit.social_auth.CoinbaseOAuth2',
)
SOCIAL_AUTH_TRAILING_SLASH = True
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)
