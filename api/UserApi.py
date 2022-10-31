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
    user_exist = User.objects(email=email).first()
    if user_exist: return { 'message': 'email is exists.' }, 303

    password = body.get('password')
    if not password: return { 'message': 'password required.' }, 400
    if len(password) < 6: return { 'message': 'password must be at least 6 characters.' }, 400
    hash_password = bcrypt.generate_password_hash(password=password).decode('utf-8')

    id = ObjectId()
    user = User(_id=id)
    user.uid = str(id)
    user.username = body.get('username')
    user.email = email
    user.password = hash_password

    try:
      user.save()
    except Exception as e:
      errors = handle_field_error(e)
      return {'message': errors}, 400
    return {'message': 'user created'}, 201