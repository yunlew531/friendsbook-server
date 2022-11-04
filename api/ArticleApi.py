from flask_restful import Resource, request

class ArticleApi(Resource):
  def post(self):
    authorization = request.headers.get('Authorization')
    if not authorization: return { 'message': 'Authorization empty' }, 401
    token = authorization.split('Bearer ')[1]
    return { 'message': 'success' }