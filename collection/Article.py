from mongoengine import Document, StringField, ObjectIdField, DateTimeField ,ListField, EmbeddedDocument, EmbeddedDocumentField, ReferenceField, QuerySet
from datetime import datetime
from collection.User import User
from bson import json_util

class Insert(EmbeddedDocument):
  image = StringField()

class Content(EmbeddedDocument):
  insert = StringField() or EmbeddedDocumentField(Insert)

class Article(Document):
  _id = ObjectIdField()
  content = ListField(EmbeddedDocumentField(Content))
  published_at = DateTimeField(default=datetime.now())
  author = ReferenceField(User, required=True)

  def to_json(self):
    data = self.to_mongo()
    del data['_id']
    data['id'] = str(self._id)
    data['author'] = {
      'username': self.author.username,
      'id': str(self.author._id)
    }
    return json_util.dumps(data)

  meta = {
    'db_alias': 'Friendsbook-alias',
    'collection': 'articles',
  }
