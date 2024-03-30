import shutil
import django_filters.rest_framework
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from rest_framework import status, generics, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.decorators import throttle_classes
from posts.models import Post
from category.models import Category
from .permissions import IsOwnerAndAdmin
from .serializers import PostGetSerializer, PostSerializer

# Create your views here.

class PostFilter(django_filters.FilterSet):
  
  category__name = django_filters.CharFilter(lookup_expr="iexact")
  author__name = django_filters.CharFilter(lookup_expr="iexact")
  is_finish = django_filters.BooleanFilter()
  id = django_filters.NumberFilter(lookup_expr="exact")
  
class PostViewSet(viewsets.ModelViewSet):
  queryset = cache.get_or_set('post', Post.objects.all())
  serializer_class = PostSerializer
  permission_classes = [IsOwnerAndAdmin]
  filter_backends = [django_filters.rest_framework.DjangoFilterBackend, OrderingFilter]
  filterset_class = PostFilter
  ordering_fields = ['wave', 'created_at']
  
  def retrieve(self, request, *args, **kwargs):
    if request.auth:
      instance = self.get_object()
    # Anonymous User reqeust retrieve post, none check object_permission step
    instance = get_object_or_404(self.queryset, **self.kwargs)
    serializer = self.get_serializer(instance)
    
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  def perform_destroy(self, instance):
    if (instance.is_finish):
      Post.changing_private(instance)
    # remove the image folder for the post
    image_storage = f'{settings.MEDIA_ROOT}/{instance.author.name}/{instance.id}'
    shutil.rmtree(image_storage, ignore_errors=True)
    instance.delete()
  
class CategoryPostView(generics.ListAPIView):
  serializer_class = PostGetSerializer
  filter_backends = [django_filters.rest_framework.DjangoFilterBackend, OrderingFilter]
  filterset_class = PostFilter
  ordering_fields = ['wave', 'created_at']
  
  def get_queryset(self):
    category_name = self.kwargs['category_name'].upper()
    category = get_object_or_404(Category, name=category_name)
    posts = Post.objects.filter(category=category)
    return posts
            