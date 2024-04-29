import os
from django.conf import settings
from rest_framework import serializers, exceptions
from django.db import models
from .models import Post
    
class PostSerializer(serializers.ModelSerializer):
  
  header_image = serializers.CharField(required=False)
  author = serializers.CharField()
  category = serializers.CharField(required=False)
  
  class Meta:
    model = Post
    fields = '__all__'
    
  
  def it_required(self, field):
    field = self.__class__.get_fields(self)[field]
    return field.required
  
  def convert_string_to_foreign_obj(self, model, field, value):
    """
    convert the foreign key to the appropriate object
    """
    try: 
      foreign_object = model.objects.get(name=value)
    except model.DoesNotExist:
      # when an model object that matches the values does not exist
      # if the required field is an error, the non-required field becomes a null value
      if self.it_required(field):
        raise exceptions.ValidationError(f'None of the {model} objects exist with name {value}')
      return None
  
    return foreign_object
  
  def validate(self, data):
    """
    Get fields related to foreign keys from the data
    convert the foreign key to the appropriate object
    """
    data_fields = data.keys()
    
    for fields in Post._meta.get_fields():
      if type(fields) == models.ForeignKey and fields.name in data_fields:
        foreign_object = self.convert_string_to_foreign_obj(fields.related_model, fields.name, data[fields.name])
        data[fields.name] = foreign_object
    
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