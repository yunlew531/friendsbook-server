from flask_restful import Resource
from flask import g
import json
import sys
sys.path.append('../..')
from collection.User import User
from flasgger import swag_from

class UserAuthApi(Resource):
  # take profile by jwt token
  @swag_from('../swagger/auth/get_user_auth.yml', methods=['GET'])
  def get(self):
    profile = json.loads(User.objects(uid=g.uid).exclude('_id', 'password').first().to_json())
    return { 'message': 'success', 'profile': profile }