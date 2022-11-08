from flask_restful import Resource, request
from flask import g
import sys
sys.path.append('../..')
from utils.handle_field_error import handle_field_error
from collection.Article import Article
from flasgger import swag_from

class ArticleAuthApi(Resource):
  @swag_from('../swagger/auth/publish_article.yml')
  def post(self):
    uid = g.uid
    body = request.get_json()
    content = body.get('content')
    if not content:
      return { 'message': 'content required', 'code': 1 }, 400  

    contentSum = ''
    for v in content:
      content = v.get('insert')
      if type(content) == dict:
        content = content.get('image', '')
      contentSum = contentSum + content.strip()
    if not contentSum:
      return { 'message': 'content is empty', 'code': 2 }, 400  

    article = Article()
    article.author_uid = uid
    article.content = content

    try:
      article.save(validate=False)
    except Exception as e:
      errors = handle_field_error(e)
      return { 'message': errors }, 500      

    return { 'message': 'success', 'data': body }