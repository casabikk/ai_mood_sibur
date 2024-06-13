from configuration.config import *
from peewee import *

connection = PostgresqlDatabase(db_name,
    user=user,
    password=password,
    host=host,
    port=port)


class BaseModel(Model):
    class Meta:
        database = connection


class Comments(BaseModel):
    platform = TextField()
    channel_id = TextField()
    name = TextField()
    user_id = TextField()
    comment_id = TextField()
    text = TextField()
    likes = IntegerField()
    date = TextField()
    mood = IntegerField()

    class Meta:
        db_table = 'Comments'
        order_by = ('id',)