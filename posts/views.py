import os
import django_filters.rest_framework
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status, generics, mixins, exceptions
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from posts.models import Post
from category.models import Category
from .permissions import IsOwnerAndAdmin
from .serializers import PostGetSerializer, PostCreateSerializer

# Create your views here.

class PostFilter(django_filters.FilterSet):
  
  category__name = django_filters.CharFilter(lookup_expr="iexact")
  author__name = django_filters.CharFilter(lookup_expr="iexact")
  is_finish = django_filters.BooleanFilter()
  id = django_filters.NumberFilter(lookup_expr="exact")

class PostView(generics.GenericAPIView, mixins.ListModelMixin):
  queryset = Post.objects.all()
  model = Post
  serializer_class = PostGetSerializer
  permission_classes = [IsOwnerAndAdmin]
  filter_backends = [django_filters.rest_framework.DjangoFilterBackend, OrderingFilter]
  filterset_class = PostFilter
  ordering_fields = ['wave', 'created_at']
  
  def permission_denied(self, request, message=None, code=None):
    """
    if request is not permitted, determine what kind of exception to raise.
    """
    if request.authenticators and not request.successful_authenticator:
        raise exceptions.NotAuthenticated(detail='로그인이 필요한 서비스입니다. 로그인을 먼저 진행해 주세요!')
    raise exceptions.PermissionDenied(detail=message, code=code)
  
  def get_object(self, **kwargs):
    obj = get_object_or_404(self.model, **kwargs)
    self.check_object_permissions(self.request, obj)
    return obj
    
  def get(self, request, *args, **kwargs):
    '''
    if an id value exists in the query, it is identified as a request for a single value
    so use PostGetSerializer and parameter many value --> False (return in array form for a definite single value is problematic)
    '''
    request_single_post = request.query_params.get('id')
    if request_single_post:
      query = {key: value for key, value in request.query_params.items()}
      post = get_object_or_404(self.model, **query)
      if request.auth:
        # when an authenticated user requests a single post --> considered permissions a required request
        # for example, when a user tries to modify a post, 
        # the person who tries to modify it and the author of the post must match to get information about that post
        self.check_object_permissions(self.request, post)
      serializer = PostGetSerializer(post)
      return Response(serializer.data, status=status.HTTP_200_OK)
    
    return self.list(request, args, kwargs)
  
  def post(self, request):
    body = request.data
    serializer = PostCreateSerializer(data=body)
    if serializer.is_valid():
      post = serializer.save()
      # is_finish = true --> this post is finally published so redirect corresponding post
      if serializer.data["is_finish"]:
        return Response({'redirect_path': f'/posts/{post.id}/', 'id': post.id}, status=status.HTTP_201_CREATED)
      return Response({'detail': '포스트가 생성되었습니다.', 'id': post.id}, status=status.HTTP_201_CREATED)
    else:
      return Response({'detail': '포스트가 생성에 실패하였습니다.', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
  
  def patch(self, request):
    body = request.data
    post_id = body.pop("id")
    post = self.get_object(id=post_id)
    serializer = PostCreateSerializer(instance=post, data=body, partial=True)
    if serializer.is_valid():
      post = serializer.save()
      # is_finish = true --> this post is already finally published so redirect corresponding post
      if post.__dict__["is_finish"]:
        return Response({'redirect_path': f'/posts/{post.id}/'}, status=status.HTTP_200_OK)
      return Response({'detail': '포스트가 임시저장되었습니다.'}, status=status.HTTP_200_OK)
    else:
      return Response({'detail': '포스트가 임시저장에 실패하였습니다.','errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
  def delete(self, request):
    body = request.data
    post_id = body.pop("id")
    post = self.get_object(id=post_id)
    # if the post is published, remove the part associated with it first
    if (post.is_finish):
        self.model.changing_private(post)
    # remove the image folder for the post
    os.rmdir(f'{settings.MEDIA_ROOT}/{post.author.name}/{post.id}')
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  
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
            