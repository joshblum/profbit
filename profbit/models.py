from datetime import datetime

from flask_login import UserMixin
from peewee import BooleanField
from peewee import CharField
from peewee import DateTimeField
from peewee import Model
from peewee import Proxy

database_proxy = Proxy()


class BaseModel(Model):
    class Meta:
        database = database_proxy


class User(BaseModel, UserMixin):
    created_at = DateTimeField(default=datetime.now)
    username = CharField(unique=True)
    email = CharField(null=True)
    active = BooleanField(default=True)

    class Meta:
        order_by = ('username',)

