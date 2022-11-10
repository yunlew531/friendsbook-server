from mongoengine import Document, StringField, IntField, ObjectIdField
from time import time

class Image(Document):
  _id = ObjectIdField()
  published_at = IntField(default=time())
  url = StringField()
  author_uid = StringField()

  meta = {
    'db_alias': 'Friendsbook-alias',
    'collection': 'images',
  }