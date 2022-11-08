from bson import ObjectId
from flask_restful import Resource, request
from flask import g
import sys
sys.path.append('../..')
from utils.handle_field_error import handle_field_error
from collection.Article import Article
from collection.User import User
from flasgger import swag_from

class ArticleAuthApi(Resource):
  @swag_from('../swagger/auth/publish_article.yml', methods=['GET'])
  def post(self):
    uid = g.uid
    body = request.get_json()
    content = body.get('content')
    if not content:
      return { 'message': 'content required', 'code': 1 }, 400  

    content_sum = ''
    for insert in content:
      v = insert.get('insert')
      if type(v) == dict:
        v = v.get('image', '')
      content_sum = content_sum + v.strip()
    if not content_sum:
      return { 'message': 'content is empty', 'code': 2 }, 400

    user = User.objects(uid=uid).first()
    user.save()

    article = Article()
    article.content = content
    article.author = user

    try:
      article.save(validate=False)
    except Exception as e:
      print(e)
      errors = handle_field_error(e)
      return { 'message': errors }, 500      

    return { 'message': 'success' }