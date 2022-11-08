from mongoengine import Document, StringField, DateTimeField, ObjectIdField
from datetime import datetime

class Image(Document):
  _id = ObjectIdField()
  published_at = DateTimeField(default=datetime.now())
  url = StringField()
  author_uid = StringField()

  meta = {
    'db_alias': 'Friendsbook-alias',
    'collection': 'images',
  }