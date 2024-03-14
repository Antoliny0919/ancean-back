import os
from django.conf import settings
from rest_framework import serializers
from users.models import User
from category.models import Category
from .models import Post
from .validators import default_errors_message

class PostGetSerializer(serializers.ModelSerializer):
  
  author = serializers.ReadOnlyField(source='author.name')
  category = serializers.ReadOnlyField(source='category.name')
  
  class Meta:
    model = Post
    fields = '__all__'
    
class PostCreateSerializer(serializers.Serializer):
  
  foreign_fields_table = {
    "author": User,
    "category": Category,
  }
  
  header_image = serializers.CharField(required=False)
  title = serializers.CharField(error_messages=default_errors_message('제목'))
  is_finish = serializers.BooleanField(error_messages=default_errors_message('is_finish'))
  author = serializers.CharField(error_messages=default_errors_message('작성자'))
  introduce = serializers.CharField(required=False)
  category = serializers.CharField(required=False)
  content = serializers.JSONField(required=False)
  
  def string_to_foreign_obj(self, **foreign_fields):
    """
    convert the foreign key to the appropriate object
    """
    
    field = {key: (self.__class__.foreign_fields_table[key]).objects.get(name=value)
          for key, value in foreign_fields.items()}

    return field
  
  def validate(self, data):
    """
    Get fields related to foreign keys from the data
    convert the foreign key to the appropriate object
    """
    fields = data.keys()
    foreign_fields = {field: data[field] for field in fields
                      if field in self.__class__.foreign_fields_table.keys()}
    
    foreign_objs = self.string_to_foreign_obj(**foreign_fields)
    for key in foreign_objs.keys():
      data[key] = foreign_objs[key]
      
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
    
    #private
    elif (before_state and not after_state):
      Post.changing_private(instance)
      
    for field_name in validated_data.keys():
      if getattr(instance, field_name) != validated_data[field_name]:
        setattr(instance, field_name, validated_data[field_name])
    
    instance.save()
      
    return instance
    
  
