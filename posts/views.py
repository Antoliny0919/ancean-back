import django_filters.rest_framework
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from users.models import User
from posts.models import Post
from .serializers import PostSerializer

# Create your views here.

class PostFilter(django_filters.FilterSet):
  
  category__name = django_filters.CharFilter(lookup_expr="iexact")
  

class PostList(ListAPIView):
  queryset = Post.objects.all()
  serializer_class = PostSerializer
  filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
  filterset_class = PostFilter

  def get_queryset(self):
    '''
    This view should return a list of all the posts
    for the user as determined by the name portion of the URL.
    '''
    username = self.kwargs['name']
    return Post.objects.filter(author__name=username)