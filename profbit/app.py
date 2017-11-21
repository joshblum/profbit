from urllib import parse

from flask import Flask
from flask import g
from flask import redirect
from flask_login import LoginManager
from flask_login import current_user
from peewee import PostgresqlDatabase
from peewee import SqliteDatabase
from raven.contrib.flask import Sentry
from social_flask.routes import social_auth
from social_flask_peewee.models import FlaskStorage
from social_flask_peewee.models import init_social

from .models import User
from .models import database_proxy

app = Flask(__name__)
app.config.from_object('profbit.settings')

# Manually enable when profiling
# from werkzeug.contrib.profiler import ProfilerMiddleware
# app.wsgi_app = ProfilerMiddleware(app.wsgi_app, sort_by=('cumtime',))

SENTRY_DSN = app.config.get('SENTRY_PRIVATE_DSN')
if not app.debug and SENTRY_DSN:
    sentry = Sentry(app, dsn=SENTRY_DSN)
else:
    sentry = None

IS_HEROKU = app.config.get('IS_HEROKU', False)
DATABASE_URL = app.config['DATABASE_URL']

if IS_HEROKU:
    parse.uses_netloc.append('postgres')
    url = parse.urlparse(DATABASE_URL)
    database = PostgresqlDatabase(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port)
    database_proxy.initialize(database)
else:
    database = SqliteDatabase(DATABASE_URL)
    database_proxy.initialize(database)

app.register_blueprint(social_auth)
init_social(app, database)

login_manager = LoginManager()
login_manager.init_app(app)


@app.cli.command()
def syncdb():
    models = [
        User,
        FlaskStorage.user,
        FlaskStorage.nonce,
        FlaskStorage.association,
        FlaskStorage.code,
        FlaskStorage.partial
    ]
    for model in models:
        model.create_table(True)


@login_manager.user_loader
def load_user(userid):
    try:
        return User.get(User.id == userid)
    except User.DoesNotExist:
        pass


@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect('/')


@app.before_request
def global_user():
    # evaluate proxy value
    g.user = current_user._get_current_object()


@app.context_processor
def inject_user():
    try:
        return {'user': g.user}
    except AttributeError:
        return {'user': None}


@app.context_processor
def inject_sentry():
    if sentry:
        return {'sentry_public_dsn': sentry.client.get_public_dsn('https')}
    return {}
