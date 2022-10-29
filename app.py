import json
from flask import Flask
from mongoengine import connect, Document, StringField
import os
from dotenv import load_dotenv
load_dotenv()
MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')

app = Flask(__name__)

connect(
  db='Friendsbook',
  host='mongodb+srv://{}:{}@friendsbook.y5tntvm.mongodb.net/?retryWrites=true&w=majority'
  .format(MONGODB_USERNAME, MONGODB_PASSWORD)
)

class User(Document):
  username = StringField(required=True)
  email = StringField(required=True)
  password = StringField(required=True, min_length=6)

@app.route('/')
def hello():
  users = User.objects().to_json()
  return users

if __name__ == '__main__':
  app.run()