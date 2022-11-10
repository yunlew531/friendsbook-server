from flask import g
from flask_restful import Resource
from collection.Article import Article
from bson import ObjectId
import json
from flasgger import swag_from

class ArticleApi(Resource):
  @swag_from('swagger/get_article.yml')
  def get(self, id):
    if len(id) != 24: return { 'message': 'article not found' }, 404
    article = Article.objects(_id=ObjectId(id)).first()
    if not article: return { 'message': 'article not found' }, 404
    article = json.loads(article.to_json())

    return { 'message': 'success', 'article': article }