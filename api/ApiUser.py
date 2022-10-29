from flask_restful import Resource, request
from bson.objectid import ObjectId
import json
import sys

sys.path.append('..')
from utils.handle_field_error import handle_field_error
from collection.User import User

class ApiUser(Resource):
  def get(self, id):
    user = json.loads(User.objects(_id=ObjectId(id)).only('username', 'email').first().to_json())
    user['uid'] = user.get('_id').get('$oid')
    del user['_id']
    return user
  def post(self):
    body = request.get_json()
    email = body.get('email')
    user_exist = User.objects(email=email).first()
    if user_exist: return { 'message': 'email is exists.' }, 303

    user = User()
    user.username = body.get('username')
    user.email = email
    user.password = body.get('password')

    try:
      user.save()
    except Exception as e:
      errors = handle_field_error(e)
      return {'message': errors}, 400
    return {'message': 'user created'}, 201