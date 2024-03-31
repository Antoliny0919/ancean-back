import os
from django.conf import settings
from rest_framework import serializers, exceptions
from django.db import models
from .models import Post
    
class PostSerializer(serializers.ModelSerializer):
  
  header_image = serializers.CharField(required=False)
  title = serializers.CharField()
  is_finish = serializers.BooleanField()
  author = serializers.CharField()
  introduce = serializers.CharField(required=False)
  category = serializers.CharField(required=False)
  content = serializers.JSONField(required=False)
  
  class Meta:
    model = Post
    fields = '__all__'
  
  def it_required(self, field):
    field = self.__class__.get_fields(self)[field]
    return field.required
  
  def convert_string_to_foreign_obj(self, **foreign_fields):
    """
    convert the foreign key to the appropriate object
    """
    converted_foreign_fields = {}
    
    for key, data in foreign_fields.items():
      try: 
        model = data['model']
        converted_foreign_fields[key] = model.objects.get(name=data['value'])
        
      except model.DoesNotExist:
        # when an model object that matches the values does not exist
        # if the required field is an error, the non-required field becomes a null value
        if self.it_required(key):
          raise exceptions.ValidationError(f'{key}에 {data["value"]}는 존재하지 않습니다.')
        converted_foreign_fields[key] = None
  
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
    if is_publish:
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