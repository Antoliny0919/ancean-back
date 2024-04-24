import os
from django.conf import settings
from rest_framework import serializers, exceptions

class ImageSerializer(serializers.Serializer):
  
  id = serializers.IntegerField(min_value=0)
  file = serializers.ImageField()
  name = serializers.CharField()
  
  
  def check_save_path(self, id, name):
    """
    the default storage path for an image --> MEDIA_ROOT/{user_name}/{post_id}/{file_name}
    verify that a path exists to store the image
    """
    user_post_store_path = os.path.join(getattr(settings, 'MEDIA_ROOT'), f'{name}/{id}')
    
    if not os.path.exists(user_post_store_path) or not id:
      raise exceptions.NotFound("이미지를 저장할 경로가 존재하지 않습니다.")
    return user_post_store_path
  
  def validate(self, data):
    """
    perform inspection to save images
    """
    id, name = data.get('id'), data.get('name')
    user_post_store_path = self.check_save_path(id, name)
    data.update({'user_post_store_path': user_post_store_path})
    
    return data
  
  
  def create(self, validated_data):
    """
    saving images to media folders
    and responding to the path and file name on which the image can be answered from the front
    
    create is the action of storing objects in a folder rather than creating objects in a model
    """
    user_post_store_path, image_file = validated_data["user_post_store_path"], validated_data["file"]
    save_path = os.path.join(user_post_store_path, image_file.name)
    with open(save_path, mode='wb') as file:
      for chunk in image_file.chunks():
        file.write(chunk)
    source_url = save_path.replace(str(getattr(settings, 'BASE_DIR')), getattr(settings, 'SERVER_URI'))
    return {'success': 1, 'file': {'url': source_url, 'name': image_file.name}}