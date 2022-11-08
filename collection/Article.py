from mongoengine import Document, StringField, ObjectIdField, DateTimeField ,ListField, EmbeddedDocument, EmbeddedDocumentField
from datetime import datetime

class Insert(EmbeddedDocument):
  image = StringField()

class Content(EmbeddedDocument):
  insert = StringField()
  insert = EmbeddedDocumentField(Insert)

class Article(Document):
  _id = ObjectIdField()
  author_uid = StringField(required=True)
  content = ListField(EmbeddedDocumentField(Content))
  published_at = DateTimeField(default=datetime.now())

  meta = {
    'db_alias': 'Friendsbook-alias',
    'collection': 'articles',
  }
