from flask import Flask
from mongoengine import connect
import os
from dotenv import load_dotenv
from flask_restful import Api
from api.AccountApi import AccountApi
from api.UsersApi import UsersApi
from api.UserApi import UserApi
from api.CheckLoginApi import CheckLoginApi
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

api.add_resource(UsersApi, '/api/users', endpoint='users')
api.add_resource(UserApi, '/api/user', '/api/user/<id>', endpoint='user')
api.add_resource(AccountApi, '/api/account', endpoint='login_logout')
api.add_resource(CheckLoginApi, '/api/account/check', endpoint='check_login')

if __name__ == '__main__':
  app.run()