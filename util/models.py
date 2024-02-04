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
    comment_id = IntegerField(unique=True)
    person_id = IntegerField()
    date = IntegerField()
    text = TextField()
    parents_stack = TextField()
    post_id = IntegerField()
    likes = IntegerField()
 
    class Meta:
        db_table = 'Comments'
        order_by = ('comment_id',)
    

class Persons(BaseModel):
    person_id = IntegerField()
    likes_count = IntegerField()
    comments_count = IntegerField()

    class Meta:
        db_table = 'Likes'
        order_by = ('like_id',)

class Mood(BaseModel):
    comment_id = IntegerField(unique=True)
    comment = TextField()
    mood = IntegerField()

    class Meta:
        db_table = 'Mood'
        order_by = ('mood_id',)