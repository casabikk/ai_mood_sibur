from models import *
from peewee import *

with connection:
    connection.create_tables([Comments])

print("Done")