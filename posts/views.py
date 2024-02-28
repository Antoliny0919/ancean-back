import django_filters.rest_framework
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, mixins
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from posts.models import Post
from category.models import Category
from .serializers import PostSerializer, PostCreateSerializer

# Create your views here.

class PostFilter(django_filters.FilterSet):
  
  category__name = django_filters.CharFilter(lookup_expr="iexact")
  is_finish = django_filters.BooleanFilter()
  id = django_filters.NumberFilter(lookup_expr="exact")
  

class PostView(generics.GenericAPIView, mixins.ListModelMixin):
  queryset = Post.objects.all()
  model = Post
  serializer_class = PostSerializer
  filter_backends = [django_filters.rest_framework.DjangoFilterBackend, OrderingFilter]
  filterset_class = PostFilter
  ordering_fields = ['wave', 'created_at']
    
  def get(self, request, *args, **kwargs):
    return self.list(request)
  
  def post(self, request):
    body = request.data
    serializer = PostCreateSerializer(data=body)
    if serializer.is_valid():
      post = serializer.save()
      # is_finish = true --> this post is finally published so redirect corresponding post
      if serializer.data["is_finish"]:
        return Response({'redirect_path': f'/posts/{post.id}/'}, status=status.HTTP_200_OK)
      return Response({'message': '포스트가 생성되었습니다.', 'id': post.id}, status=status.HTTP_200_OK)
    else:
      return Response({'message': '포스트가 생성에 실패하였습니다.', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
  
  def patch(self, request):
    body = request.data
    post_id = body.pop("id")
    existing_post = get_object_or_404(Post, id=post_id)
    serializer = PostCreateSerializer(instance=existing_post, data=body, partial=True)
    if serializer.is_valid():
      post = serializer.save()
      # is_finish = true --> this post is already finally published so redirect corresponding post
      if post.__dict__["is_finish"]:
        return Response({'redirect_path': f'/posts/{post.id}/'}, status=status.HTTP_200_OK)
      return Response({'message': '포스트가 임시저장되었습니다.'}, status=status.HTTP_200_OK)
    else:
      return Response({'message': '포스트가 임시저장에 실패하였습니다.','errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
  def delete(self, request):
    body = request.data
    post_id = body.pop("id")
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
  
  
class CategoryPostView(generics.ListAPIView):
  serializer_class = PostSerializer
  filter_backends = [django_filters.rest_framework.DjangoFilterBackend, OrderingFilter]
  filterset_class = PostFilter
  ordering_fields = ['wave', 'created_at']
  
  def get_queryset(self):
    category_name = self.kwargs['category_name'].upper()
    category = get_object_or_404(Category, name=category_name)
    posts = Post.objects.filter(category=category)
    return posts
            