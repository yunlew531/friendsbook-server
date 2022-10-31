from flask_restful import Resource, request
import jwt
import os

class CheckLoginApi(Resource):
  def get(self):
    authorization = request.headers.get('Authorization')
    try:
      uid = jwt.decode(authorization, os.getenv('JWT_KEY'), algorithms=['HS256']).get('uid')
    except jwt.exceptions.DecodeError as e:
      return { 'message': str(e) }, 400
    return { 'message': 'success', 'uid': uid }