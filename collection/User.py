from mongoengine import Document, StringField, EmailField

class User(Document):
  _id = StringField()
  username = StringField(required=True, min_length=2)
  email = EmailField(required=True)
  password = StringField(required=True, min_length=6)
