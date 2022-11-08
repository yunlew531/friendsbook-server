from flask import Flask, request, g
from mongoengine import connect
import os
from dotenv import load_dotenv
from flask_restful import Api
from api.AccountApi import AccountApi, CheckLoginApi
from api.UsersApi import UsersApi
from api.UserApi import UserApi
from api.auth.UserAuthApi import UserAuthApi
from api.auth.ImageAuthApi import ImageAuthApi
from api.auth.ArticleAuthApi import ArticleAuthApi
import jwt
load_dotenv()
from flasgger import Swagger
from flask_cors import CORS
MONGODB_USERNAME = os.getenv('MONGODB_USERNAME')
MONGODB_PASSWORD = os.getenv('MONGODB_PASSWORD')

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": ['http://localhost:3000']}})
api = Api(app)

# firebase
from firebase import Firebase
config = {
  "apiKey": os.getenv('apiKey'),
  "authDomain": os.getenv('authDomain'),
  "databaseURL": os.getenv('databaseURL'),
  "storageBucket": os.getenv('storageBucket'), 
  "serviceAccount": "serviceAccountKey.json"
}
firebase = Firebase(config)
storage = firebase.storage()

# swagger
app.config['SWAGGER'] = {
  "title": "Friendsbook API",
  "description": "server: https://github.com/yunlew531/friendsbook-server\nfrontend: https://github.com/yunlew531/friendsbook",
  "version": "1.0",
  "termsOfService": "",
  "hide_top_bar": True,
}
Swagger(app)

# mongoDB
connect(
  db='Friendsbook',
  alias='Friendsbook-alias',
  host='mongodb+srv://{}:{}@friendsbook.y5tntvm.mongodb.net/?retryWrites=true&w=majority'
    .format(MONGODB_USERNAME, MONGODB_PASSWORD)
)

# before every request (method 'OPTIONS' also include)
@app.before_request
def checkAuth():
  if request.method == 'OPTIONS': return None
  isAuth = '/api/auth/' in request.path
  if isAuth:
    authorization = request.headers.get('Authorization')
    if not authorization: return { 'message' : 'Authorization empty' }, 401
    if not 'Bearer ' in authorization: return { 'message' : 'Authorization invalid' }, 403
    token = authorization.split('Bearer ')[1]
    try:
      uid = jwt.decode(token, os.getenv('JWT_KEY'), algorithms=['HS256']).get('uid')
    except Exception as e:
      return { 'message': e }, 403
    g.uid = uid

# api
api.add_resource(UsersApi, '/api/users', endpoint='users')
api.add_resource(UserApi, '/api/user/<uid>', methods=['GET'], endpoint='user')
api.add_resource(UserApi, '/api/user', methods=['POST'], endpoint='create_user')
api.add_resource(AccountApi, '/api/account/logout', methods=['GET'], endpoint='logout')
api.add_resource(AccountApi, '/api/account/login', methods=['POST'], endpoint='login')

# auth
api.add_resource(CheckLoginApi, '/api/auth/check', endpoint='check')
api.add_resource(UserAuthApi, '/api/auth/user', methods=['GET'], endpoint='user_auth')
api.add_resource(ImageAuthApi, '/api/auth/image/upload', methods=['POST'], endpoint='image_upload')
api.add_resource(ArticleAuthApi, '/api/auth/article', methods=['POST'], endpoint='article_publish')

if __name__ == '__main__':
  app.run()