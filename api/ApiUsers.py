from mongoengine import Document, StringField
from flask_restful import Resource, request
import sys
sys.path.append("..")
from collection.User import User
import json

class ApiUsers(Resource):
  def get(self):
    users = json.loads(User.objects().to_json())
    for user in users:
      user['uid'] = user.get('_id').get('$oid')
      del user['_id']
    return users