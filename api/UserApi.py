from flask_restful import Resource, request
from bson.objectid import ObjectId
import json
import sys
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
sys.path.append('..')
from utils.handle_field_error import handle_field_error
from collection.User import User
from flasgger import swag_from

class UserApi(Resource):
  # take profile by uid
  @swag_from('swagger/get_user.yml', methods=['GET'])
  def get(self, uid):
    user = User.objects(uid=uid).only('username', 'email', 'uid').exclude('_id').first()
    if not user: return { 'message': 'user not found' }, 404
    user = json.loads(user.to_json())
    return { 'message': 'success', 'user': user }

  @swag_from('swagger/create_user.yml', methods=['POST'])
  def post(self):
    body = request.get_json()
    email = body.get('email')
    username = body.get('username')
    user_exist = User.objects(email=email).first()
    if not username: return { 'message': 'username required.', 'code': 2 }, 400
    if not email: return { 'message': 'email required.', 'code': 3 }, 400
    if user_exist: return { 'message': 'email is exists.', 'code': 1 }, 303

    password = body.get('password')
    if not password: return { 'message': 'password required.', 'code': 4 }, 400
    if type(password) != str: return { 'message': 'password invalid', 'code': 5 }, 400
    hash_password = bcrypt.generate_password_hash(password=password).decode('utf-8')

    id = ObjectId()
    user = User(_id=id)
    user.uid = str(id)
    user.username = username
    user.email = email
    user.password = hash_password

    try:
      user.save()
    except Exception as e:
      errors = handle_field_error(e)
      email_error = errors.get('email')
      password_error = errors.get('password')
      username_error = errors.get('username')

      if email_error:
        if 'Invalid email address' in errors.get('email'): return {'message': 'email invalid', 'code': 6}, 400
      if username_error:
        if 'StringField only accepts string values' in username_error:
          return {'message': username_error, 'code': 7}, 400
        if 'String value is too short': return {'message': username_error, 'code': 8}, 400
      if password_error: 
        if 'String value is too short' in password_error: return {'message': password_error, 'code': 9}, 400
      return {'message': errors}, 400
    return {'message': 'user created'}, 201