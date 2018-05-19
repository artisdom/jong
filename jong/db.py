# coding: utf-8
import peewee
from jong import settings

DATABASE_CONNECTION = peewee.SqliteDatabase(settings.JONG_DB)


class BaseModel(peewee.Model):
    class Meta:
        database = DATABASE_CONNECTION


class Rss(BaseModel):
    """
    RSS Model
    """
    id = peewee.PrimaryKeyField()
    name = peewee.CharField(max_length=200, unique=True)
    notebook = peewee.CharField(max_length=200, null=False)
    url = peewee.CharField(max_length=500, null=False)
    tag = peewee.CharField(max_length=40, null=True)
    date_triggered = peewee.DateTimeField(null=True)
    status = peewee.BooleanField(default=True)


for model in (Rss, ):
    try:
        model.create_table()
    except:
        pass