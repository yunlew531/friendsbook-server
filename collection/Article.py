from mongoengine import Document, StringField, ObjectIdField, IntField, EmbeddedDocument, EmbeddedDocumentField, ReferenceField, NULLIFY, EmbeddedDocumentListField
from time import time
from collection.User import User
from bson import ObjectId, json_util

class Insert(EmbeddedDocument):
  image = StringField()

class Content(EmbeddedDocument):
  insert = StringField() or EmbeddedDocumentField(Insert)

class ThumbsUp(EmbeddedDocument):
  _id = ObjectIdField(primary_key=True, default=ObjectId())
  author = ReferenceField(User)
  uid = StringField()

class Article(Document):
  _id = ObjectIdField()
  author = ReferenceField(User, required=True, reverse_delete_rule=NULLIFY)
  uid = StringField()
  content = EmbeddedDocumentListField(Content)
  published_at = IntField(default=time())
  thumbs_up = EmbeddedDocumentListField(ThumbsUp, default=[])

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
