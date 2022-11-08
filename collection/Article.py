from mongoengine import Document, StringField, ObjectIdField, IntField ,ListField, EmbeddedDocument, EmbeddedDocumentField, ReferenceField, NULLIFY
from time import time
from collection.User import User
from bson import json_util

class Insert(EmbeddedDocument):
  image = StringField()

class Content(EmbeddedDocument):
  insert = StringField() or EmbeddedDocumentField(Insert)

class Article(Document):
  _id = ObjectIdField()
  content = ListField(EmbeddedDocumentField(Content))
  published_at = IntField(default=time())
  author = ReferenceField(User, required=True, reverse_delete_rule=NULLIFY)

  def to_json(self):
    data = self.to_mongo()
    del data['_id']
    data['id'] = str(self._id)
    if self.author:
      data['author'] = {
        'username': self.author.username,
        'id': str(self.author._id)
      }
    return json_util.dumps(data)

  meta = {
    'db_alias': 'Friendsbook-alias',
    'collection': 'articles',
  }
