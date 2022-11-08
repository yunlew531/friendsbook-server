from flask_restful import Resource, request
from flask import g
import sys
from bson.objectid import ObjectId
from utils.handle_field_error import handle_field_error
sys.path.append('../..')
from collection.Image import Image
from flasgger import swag_from

class ImageAuthApi(Resource):
  # upload image
  @swag_from('../swagger/auth/upload_image.yml')
  def post(self):
    from app import storage
    file = request.files.get('image-file')
    if not file.filename.endswith('.jpeg') and not file.filename.endswith('.jpg'):
      return { 'message': 'jpg or jpeg only', 'code': 1 }, 400

    uid = g.uid
    id = ObjectId()
    ref = storage.child('{0}/{1}'.format(uid, str(id)))
    ref.put(file, uid)
    url = storage.child('{0}/{1}'.format(uid, str(id))).get_url(None)
    image = Image(_id=id)
    image.url = url
    image.author_uid = uid

    try:
      image.save()
    except Exception as e:
      errors = handle_field_error(e)
      return { 'message': errors }, 500      

    return { 'message': 'success', 'url': url }