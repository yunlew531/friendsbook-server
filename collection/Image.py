from mongoengine import Document, StringField, DateTimeField, ObjectIdField

class Image(Document):
  _id = ObjectIdField()
  published_at = DateTimeField()
  url = StringField()
  author_uid = StringField()

  meta = {
    'db_alias': 'Friendsbook-alias',
    'collection': 'images',
  }