from mongoengine import Document, StringField, DateTimeField, ObjectIdField
from time import time

class Image(Document):
  _id = ObjectIdField()
  published_at = DateTimeField(default=time())
  url = StringField()
  author_uid = StringField()

  meta = {
    'db_alias': 'Friendsbook-alias',
    'collection': 'images',
  }