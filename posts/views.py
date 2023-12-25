import django_filters.rest_framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from posts.models import Post
from .serializers import PostSerializer
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
    
    serializer = PostView.serializer_class(data=body)
    
    if serializer.is_valid():
      title = body.pop("title")
      is_finish = body.pop("is_finish")
      post = Post.objects.create_post(title, is_finish, **body)
      return Response(post, status=status.HTTP_200_OK)
            
  def patch(self, request):
    body = request.data
    


class PostTestView(APIView):
  
  def post(self, request):
    body = request.data
    
    serializer = PostSerializer(data=body)
    if serializer.is_valid():
      state = body['state']
      if state == 'create':
        
        Post.objects.create_post(**body, is_finish=True, is_public=True)
        return Response({'status': 'create'}, status=status.HTTP_201_CREATED)
      elif state == 'save':
        
        Post.objects.save_post(**body)
        return Response({'status': 'save'}, status=status.HTTP_200_OK)
      
    else:
      return Response({'status': 'fail'}, status=status.HTTP_400_BAD_REQUEST)