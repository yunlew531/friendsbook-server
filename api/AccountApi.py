from flask_restful import Resource, request
from flask import g
import sys
sys.path.append('..')
import json
from collection.User import User
from flask_bcrypt import Bcrypt
import os
import jwt
import datetime
from flasgger import swag_from
bcrypt = Bcrypt()

class AccountApi(Resource):
  # logout
  @swag_from('swagger/logout.yml')
  def get(self):
    return { 'message': 'success' }
  # login
  @swag_from('swagger/login.yml')
  def post(self):
    body = request.get_json()
    email = body.get('email')
    password = body.get('password')
    if not email: return { 'message': 'email required.', 'code': 1 }, 400
    if not password: return { 'message': 'password required.', 'code': 2 }, 400
    if len(password) < 6: return { 'message': 'password must be at least 6 characters.', 'code': 3 }, 400
    
    user = User.objects(email=email).only('password', 'uid', 'username').first()
    if not user: return { 'message': 'user not found.', 'code': 4 }, 404
    user = json.loads(user.to_json())
    hash_password = user.get('password')
    is_password_valid = bcrypt.check_password_hash(hash_password, password)
    if not is_password_valid: return { 'message': 'password is wrong.', 'code': 5}, 400
    uid = user.get('uid')
    username = user.get('username')
    jwt_exp = datetime.datetime.now()+ datetime.timedelta(days=7)
    jwt_token = jwt.encode({'uid': uid, 'username': username, 'exp': jwt_exp}, os.getenv('JWT_KEY'), algorithm="HS256")
    return { 'message': 'success', 'token': jwt_token, 'uid': uid }

class CheckLoginApi(Resource):
  @swag_from('swagger/check_login.yml')
  def get(self):
    uid = g.uid
    if not uid: return { 'message': 'Authorization invalid' }
    return { 'message': 'success', 'uid': uid }