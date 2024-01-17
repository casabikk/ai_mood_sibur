from models import *
from peewee import *
from comments_loading import person, comments


with connection:
    Persons.insert_many(person).execute()
    Comments.insert_many(comments).execute()

print("Done")