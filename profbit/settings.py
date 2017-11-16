import os

SECRET_KEY = os.environ.get('SECRET_KEY', '')
IS_HEROKU = os.environ.get('IS_HEROKU', False)
FLASK_DEBUG = not IS_HEROKU
DATABASE_URL = os.environ.get('DATABASE_URL', '/tmp/profbit.db')
SENTRY_PUBLIC_DSN = os.environ.get('SENTRY_PUBLIC_DSN', '')

# For templates
LOGIN_URL = "/login/coinbase/?remember_me=1"

# Flask Login
SESSION_COOKIE_NAME = 'psa_session'
USE_SESSION_FOR_NEXT = True

# Social Auth
SOCIAL_AUTH_COINBASE_GET_ALL_EXTRA_DATA = True
SOCIAL_AUTH_REMEMBER_SESSION_NAME = 'remember_me'
SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['remember_me']
SOCIAL_AUTH_COINBASE_KEY = os.environ.get('SOCIAL_AUTH_COINBASE_KEY', '')
SOCIAL_AUTH_COINBASE_SECRET = os.environ.get('SOCIAL_AUTH_COINBASE_SECRET', '')
SOCIAL_AUTH_COINBASE_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_COINBASE_SCOPE = [
        'wallet:accounts:read', 'wallet:transactions:read', 'wallet:user:read']
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
