from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from posts.models import Post
from .models import Category
from .serializer import CategorySerializer
from posts.serializers import PostSerializer

# Create your views here.

class CategoryView(APIView):
  '''
  get categories in the order of many posters by category
  '''
  
  def get(self, request):
    RepresentativeCategory = Category.objects.all().order_by('-post_count')
    serializer = CategorySerializer(RepresentativeCategory, many=True)
    return Response(serializer.data, status.HTTP_200_OK)

class CategoryPostView(APIView):
  '''
  get posts by category
  '''
  
  def get(self, request, category_name):
    category = get_object_or_404(Category, name=category_name.upper())
    posts = Post.objects.filter(category=category).order_by('-wave')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status.HTTP_200_OK)