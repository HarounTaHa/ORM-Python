from model import Model
from field import *
from database import Database

Model.db = Database('database.sqlite')
Model.connection = Model.db.connect()


class Post(Model):
    title = CharField()
    body = TextField()
    created_at = DateTimeField()
    published = BooleanField()


class User(Model):
    first_name = CharField()
    last_name = CharField(max_length=255)
    age = IntegerField()


if __name__ == '__main__':
    post = Post()
