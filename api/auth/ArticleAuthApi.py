from bson import ObjectId
from flask_restful import Resource, request
from flask import g
import sys
sys.path.append('../..')
from utils.handle_field_error import handle_field_error
from collection.Article import Article, ThumbsUp
from collection.User import User
from flasgger import swag_from

class ArticleAuthApi(Resource):
  # publish article on personal page
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
    article.uid = g.uid

    try:
      article.save(validate=False)
    except Exception as e:
      return { 'message': handle_field_error(e) }, 500      

    return { 'message': 'success' }

class ArticleThumbsUpApi(Resource):
  def post(self, article_id):
    if not len(article_id) == 24: return { 'message': 'article not found' }, 404
    article = Article.objects(_id=ObjectId(article_id)).first()
    if not article: return {'message': 'article not found' }, 404
    user = User.objects(_id=ObjectId(g.uid)).first()
    user.save()

    thumbs_up_exist = article.thumbs_up.filter(uid= g.uid)
    if thumbs_up_exist: thumbs_up_exist.delete()
    else: 
      thumbsup = ThumbsUp(uid=g.uid)
      article.thumbs_up.append(thumbsup)    
    try:
      article.save()
    except Exception as e:
      print(e)
      return {'message': handle_field_error(e) }, 500

    return {'message':'success' }