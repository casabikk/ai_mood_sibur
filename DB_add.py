from util.models import *
from peewee import *
from vk_comments_loading import person, comments

def db_add_person(person):
    with connection:
        Persons.insert_many(person).execute()

def db_add_comments(comments):
    with connection:
        Comments.insert_many(comments).execute()


def db_add_moods(moods):
    with connection:
        Mood.insert_many(moods).execute()