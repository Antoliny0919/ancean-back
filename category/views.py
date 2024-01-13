import django_filters.rest_framework
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.filters import OrderingFilter
from posts.models import Post
from .models import Category
from .serializer import CategorySerializer
from posts.serializers import PostSerializer

# Create your views here.

class CategoryView(GenericAPIView, ListModelMixin):
  '''
  get categories in the order of many posters by category
  '''
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  filter_backends = [django_filters.rest_framework.DjangoFilterBackend, OrderingFilter]
  ordering_fields = ['post_count']
  
  def get(self, request, *args, **kwargs):
    return self.list(request)

class CategoryPostView(APIView):
  '''
  get posts by category
  '''
  
  def get(self, request, category_name):
    category = get_object_or_404(Category, name=category_name.upper())
    posts = Post.objects.filter(category=category).order_by('-wave')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data, status.HTTP_200_OK)