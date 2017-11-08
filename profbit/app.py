from urllib import parse

from flask import Flask
from flask import g
from flask_login import LoginManager
from flask_login import current_user
from peewee import PostgresqlDatabase
from peewee import SqliteDatabase
from social_flask.routes import social_auth
from social_flask_peewee.models import FlaskStorage
from social_flask_peewee.models import init_social

from .models import User
from .models import database_proxy

app = Flask(__name__)
app.config.from_object('profbit.settings')

IS_HEROKU = app.config['IS_HEROKU']
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
