from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
  # header_image = serializers.ImageField(use_url=True)
  author = serializers.StringRelatedField()
  category = serializers.StringRelatedField()
  
  class Meta:
    model = Post
    fields = '__all__'