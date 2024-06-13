from models import *
from peewee import *

def db_add_comments(comments):
    with connection:
        Comments.insert_many(comments).execute()
