from flask import Flask
from mongoengine import connect
import os
from dotenv import load_dotenv
from flask_restful import Api
from api.ApiAccount import ApiAccount
from api.ApiUsers import ApiUsers
from api.ApiUser import ApiUser
load_dotenv()
MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')

app = Flask(__name__)
api = Api(app)

connect(
  db='Friendsbook',
  alias='Friendsbook-alias',
  host='mongodb+srv://{}:{}@friendsbook.y5tntvm.mongodb.net/?retryWrites=true&w=majority'
    .format(MONGODB_USERNAME, MONGODB_PASSWORD)
)

api.add_resource(ApiUsers, '/api/users')
api.add_resource(ApiUser, '/api/user', '/api/user/<id>')
api.add_resource(ApiAccount, '/api/account')

if __name__ == '__main__':
  app.run()