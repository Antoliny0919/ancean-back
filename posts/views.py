import django_filters.rest_framework
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from posts.models import Post
from .serializers import PostSerializer

# Create your views here.

class PostFilter(django_filters.FilterSet):
  
  category__name = django_filters.CharFilter(lookup_expr="iexact")
  

class PostView(GenericAPIView, ListModelMixin, CreateModelMixin):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  filter_backends = [django_filters.rest_framework.DjangoFilterBackend, OrderingFilter]
  filterset_class = PostFilter
  ordering_fields = ['wave', 'created_at']
  
  def get(self, request, *args, **kwargs):
    return self.list(request)
    
  def post(self, request, *args, **kwargs):
    print(request.data)    
    return self.create(request)
  