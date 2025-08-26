import peewee
from ycaro_airlines_v2.app import db


class BaseModel(peewee.Model):
    class Meta:
        database = db
