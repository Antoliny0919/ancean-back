from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from rest_framework import serializers
from users.models import User
from category.models import Category
from .models import Post
from .validators import default_errors_message

class PostSerializer(serializers.ModelSerializer):
  
  author = serializers.StringRelatedField()
  category = serializers.StringRelatedField()
  
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
    try:
      foreign_objs = self.string_to_foreign_obj(**foreign_fields)
      for key in foreign_objs.keys():
        data[key] = foreign_objs[key]
        
      return data
    
    except ObjectDoesNotExist:
      raise serializers.ValidationError("Object matching received data does not exist")
    
  def create(self, validated_data):
    
    post = Post.objects.create_post(**validated_data)
    return post

  def update(self, instance, validated_data):
    '''
    Replace only the other values between the field values of the 
    existing data and POST body data
    '''
    
    post = Post.objects.save_post(instance, **validated_data)
    return post
    
  
