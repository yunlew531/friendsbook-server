from mongoengine import Document, StringField, EmailField, ObjectIdField

class User(Document):
  _id = ObjectIdField()
  uid = StringField()
  username = StringField(required=True, min_length=2)
  email = EmailField(required=True)
  password = StringField(required=True, min_length=6)
