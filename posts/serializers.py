from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from users.models import User
from category.models import Category
from .models import Post

class PostSerializer(serializers.ModelSerializer):
  # header_image = serializers.ImageField(use_url=True)
  author = serializers.StringRelatedField()
  category = serializers.StringRelatedField()
  
  class Meta:
    model = Post
    fields = '__all__'
    
class PostCreateSerializer(serializers.ModelSerializer):
  
  foreign_fields_table = {
    "author": User,
    "category": Category,
  }

  title = serializers.CharField(required=True)
  is_finish = serializers.BooleanField(required=True)
  author = serializers.CharField()
  category = serializers.CharField()
  
  class Meta:
    model = Post
    fields = '__all__'
  
  def string_to_foreign_obj(self, **foreign_fields):

    field = {key: (self.__class__.foreign_fields_table[key]).objects.get(name=value)
            for key, value in foreign_fields.items()}

    return field
  
  def validate(self, data):
    """
    Check that start is before finish.
    """
    fields = data.keys()
    
    foreign_fields = {field: data[field] for field in fields
                      if field in self.__class__.foreign_fields_table.keys()}
    try:
      foreign_objs = self.string_to_foreign_obj(**foreign_fields)
      for key in foreign_objs.keys():
        data[key] = foreign_objs[key]
        
      return data
    
    except ObjectDoesNotExist:
      raise serializers.ValidationError("Does not exist foreign key object")
    
  def create(self, validated_data):
    post = Post.objects.create_post(**validated_data)
    return post
    
  
