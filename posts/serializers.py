import os
from django.conf import settings
from rest_framework import serializers
from django.db import models
from .models import Post
from .validators import default_errors_message

class PostGetSerializer(serializers.ModelSerializer):
  
  author = serializers.ReadOnlyField(source='author.name')
  category = serializers.ReadOnlyField(source='category.name')
  
  class Meta:
    model = Post
    fields = '__all__'
    
class PostCreateSerializer(serializers.Serializer):
  
  header_image = serializers.CharField(required=False)
  title = serializers.CharField(error_messages=default_errors_message('제목'))
  is_finish = serializers.BooleanField(error_messages=default_errors_message('is_finish'))
  author = serializers.CharField(error_messages=default_errors_message('작성자'))
  introduce = serializers.CharField(required=False)
  category = serializers.CharField(required=False)
  content = serializers.JSONField(required=False)
  
  def convert_string_to_foreign_obj(self, **foreign_fields):
    """
    convert the foreign key to the appropriate object
    """
    converted_foreign_fields = {}
    
    for key, data in foreign_fields.items():
      try: 
        model = data['model']
        # check field name property have setter 
        if hasattr(model, '_name'):
          converted_foreign_fields[key] = model.objects.get(_name=data['value'])
        else:
          converted_foreign_fields[key] = model.objects.get(name=data['value'])
        
      except model.DoesNotExists:
        raise f'{key}에 {data["value"]}는 존재하지 않습니다.'
  
    return converted_foreign_fields
  
  def validate(self, data):
    """
    Get fields related to foreign keys from the data
    convert the foreign key to the appropriate object
    """
    foreign_fields = {}
    data_fields = data.keys()
    
    for fields in Post._meta.get_fields():
      if type(fields) == models.ForeignKey and fields.name in data_fields:
        foreign_fields[fields.name] = {'model': fields.related_model, 'value': data[fields.name]}
    
    converted_foreign_fields = self.convert_string_to_foreign_obj(**foreign_fields)
    for key in converted_foreign_fields.keys():
      data[key] = converted_foreign_fields[key]
      
    return data
    
  def create(self, validated_data):
    
    is_publish = validated_data["is_finish"]
    if (is_publish):
      validated_data = Post.changing_public(instance=None, **validated_data)
    
    post = Post.objects.create(**validated_data)
    # create a folder in the media folder for storing images associated with the created post
    os.mkdir(f'{settings.MEDIA_ROOT}/{post.author.name}/{post.id}/')
    return post

  def update(self, instance, validated_data):
    '''
    Replace only the other values between the field values of the 
    existing data and POST body data
    '''
    
    before_state = getattr(instance, "is_finish")
    after_state = validated_data["is_finish"]
    
    # public
    if (not before_state and after_state):
      validated_data = Post.changing_public(instance, **validated_data)
    
    # private
    elif (before_state and not after_state):
      Post.changing_private(instance)
      
    for field_name in validated_data.keys():
      if getattr(instance, field_name) != validated_data[field_name]:
        setattr(instance, field_name, validated_data[field_name])
    
    instance.save()
      
    return instance
    
  
