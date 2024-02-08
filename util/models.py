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
    platform_flag = IntegerField()
    text = TextField()
    likes = IntegerField()
    date = IntegerField()
    mood = IntegerField()
    
    class Meta:
        db_table = 'Comments'
        order_by = ('id',)
    

class Persons(BaseModel):
    person_id = IntegerField()
    likes_count = IntegerField()
    comments_count = IntegerField()

    class Meta:
        db_table = 'Likes'
        order_by = ('like_id',)

class Mood(BaseModel):
    id = IntegerField()
    comment = TextField()
    mood = IntegerField()

    class Meta:
        db_table = 'Mood'
        order_by = ('comment_id',)