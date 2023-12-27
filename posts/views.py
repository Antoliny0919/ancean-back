import django_filters.rest_framework
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from posts.models import Post
from .serializers import PostSerializer, PostCreateSerializer

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
  
  def post(self, request):
    body = request.data
    print(body)
    serializer = PostCreateSerializer(data=body)
    if serializer.is_valid():
      post = serializer.save()
      return Response({'id': post.id}, status=status.HTTP_200_OK)
    else:
      return Response({'message': '포스트 생성 실패.', 'errors': serializer.errors})
            
  def patch(self, request):
    body = request.data
    post_id = body.pop("id")
    existing_post = get_object_or_404(Post, id=post_id)
    serializer = PostCreateSerializer(instance=existing_post, data=body, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response({'message': '저장 성공!'}, status=status.HTTP_200_OK)
    else:
      return Response({'message': '저장 실패!', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class PostTestView(APIView):
  
  def post(self, request):
    body = request.data
    
    serializer = PostCreateSerializer(data=body)
    if serializer.is_valid():
      # print(serializer.data)
      serializer.save()
      return Response({"hello": "world"}, status=status.HTTP_200_OK)
            