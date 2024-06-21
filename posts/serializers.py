import os
from django.conf import settings
from rest_framework import serializers
from .models import Post
from users.models import User
from category.models import Category
    
class PostSerializer(serializers.ModelSerializer):
  
  header_image = serializers.CharField(required=False)
  author = serializers.SlugRelatedField(slug_field="name", queryset=User.objects.all())
  category = serializers.SlugRelatedField(slug_field="name", queryset=Category.objects.all(), required=False)
  
  class Meta:
    model = Post
    fields = '__all__'
  
  def validate(self, data):
    
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