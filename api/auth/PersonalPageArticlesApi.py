from flask import g
from flask_restful import Resource
from collection.Article import Article
from bson import ObjectId
import json
from flasgger import swag_from

class PersonalPageArticlesApi(Resource):
  @swag_from('../swagger/auth/get_personal_page_articles.yml')
  def get(self):
    uid = g.uid
    articles = Article.objects('author._id'==ObjectId(uid))
    articles_list = []
    for article in articles:
      articles_list.append(json.loads(article.to_json()))

    return { 'message': 'success', 'articles': articles_list }