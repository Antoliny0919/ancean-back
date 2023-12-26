import django_filters.rest_framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from posts.models import Post
from .serializers import PostSerializer, PostCreateSerializer
from users.models import User
from category.models import Category

# Create your views here.

class PostFilter(django_filters.FilterSet):
  
  category__name = django_filters.CharFilter(lookup_expr="iexact")
  

class PostView(GenericAPIView, ListModelMixin):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  filter_backends = [django_filters.rest_framework.DjangoFilterBackend, OrderingFilter]
  filterset_class = PostFilter
  ordering_fields = ['wave', 'created_at']
  
  def get(self, request, *args, **kwargs):
    return self.list(request)
  
  # doesn't have post
  def post(self, request):
    body = request.data
    serializer = PostCreateSerializer(data=body)
    if serializer.is_valid():
      post = serializer.save()
      return Response({'id': post.id}, status=status.HTTP_200_OK)
            
  # def patch(self, request):
  #   body = request.data
    
  #   serializer = self.__class__.serializer_class(data=body)
    
  #   if serializer.is_valid():
  #     post = Post.objects.save_post()


class PostTestView(APIView):
  
  def post(self, request):
    body = request.data
    print(body)
    serializer = PostCreateSerializer(data=body)
    if serializer.is_valid():
      # print(serializer.data)
      serializer.save()
      return Response({"hello": "world"}, status=status.HTTP_200_OK)
            