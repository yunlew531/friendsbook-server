from flask import Flask
from mongoengine import connect
import os
from dotenv import load_dotenv
from flask_restful import Api
from api.AccountApi import AccountApi, CheckLoginApi
from api.UsersApi import UsersApi
from api.UserApi import UserApi
load_dotenv()
from flasgger import Swagger
MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')

app = Flask(__name__)
api = Api(app)

app.config['SWAGGER'] = {
    "title": "Friendsbook API",
    "description": "server: https://github.com/yunlew531/friendsbook-server\nfrontend: https://github.com/yunlew531/friendsbook",
    "version": "1.0.2",
    "termsOfService": "",
    "hide_top_bar": True,
}
Swagger(app)

connect(
  db='Friendsbook',
  alias='Friendsbook-alias',
  host='mongodb+srv://{}:{}@friendsbook.y5tntvm.mongodb.net/?retryWrites=true&w=majority'
    .format(MONGODB_USERNAME, MONGODB_PASSWORD)
)

api.add_resource(UsersApi, '/api/users', endpoint='users')
api.add_resource(UserApi, '/api/user/<uid>', methods=['GET'], endpoint='user')
api.add_resource(UserApi, '/api/user', methods=['POST'], endpoint='create_user')
api.add_resource(AccountApi, '/api/account', endpoint='account')
api.add_resource(CheckLoginApi, '/api/account/check', endpoint='check')

if __name__ == '__main__':
  app.run()