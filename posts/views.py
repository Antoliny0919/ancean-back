from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User
from posts.models import Post
from .serializers import PostSerializer

# Create your views here.

class PostView(APIView):
  
  def get(self, request, name):
    
    author = get_object_or_404(User, name=name)
    posts = author.post.all()
    serializer = PostSerializer(posts, many=True, context= {'request' : request})
    return Response(serializer.data, status=status.HTTP_200_OK)
  
  # def post(self, request):
    
    