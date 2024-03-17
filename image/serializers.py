import os
from django.conf import settings
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import serializers

class ImageSerializer(serializers.Serializer):
  
  file = serializers.ImageField()
  id = serializers.IntegerField()
  name = serializers.CharField()
  
  
  def check_save_path(self, id, name):
    user_post_store_path = os.path.join(getattr(settings, 'MEDIA_ROOT'), f'{name}/{id}')
    
    if not os.path.exists(user_post_store_path) or not id:
      raise FileNotFoundError(f'{user_post_store_path} 이미지를 저장할 경로가 존재하지 않습니다.')
    return user_post_store_path
  
  def validate(self, data):
    """
    """
    id, name = data.get('id'), data.get('name')
    user_post_store_path = self.check_save_path(id, name)
    data.update({'user_post_store_path': user_post_store_path})
    
    return data
  
  
  def create(self, validated_data):
    
    user_post_store_path, image_file = validated_data["user_post_store_path"], validated_data["file"]
    save_path = os.path.join(user_post_store_path, image_file.name)
    
    with open(save_path, mode='wb') as file:
      for chunk in image_file.chunks():
        file.write(chunk)
        
    source_url = save_path.replace(str(getattr(settings, 'MAIN_DIR')), getattr(settings, 'SERVER_URI'))
    
    return {'success': 1, 'file': {'url': source_url, 'name': image_file.name}}