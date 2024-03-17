import os
from django.conf import settings
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from .serializers import ImageSerializer


# Create your views here.

class ImageView(views.APIView):
  
  permission_classes = [IsAdminUser]
  
  def post(self, request):
    '''
    save the image requested  by the user
    path design --> '/ancean/media/{user_name}/{post_number(id)}/{file_name}'
    the id value of the post is required to save the image(it's mean image save only when post is created)
    '''
    data = request.data
    kwargs = {'file': data.get('file'), 'id': data.get('id'), 'name': request.user.name}
    serializer = ImageSerializer(data=kwargs)
    
    if serializer.is_valid(raise_exception=True):
      response = serializer.save()
      return Response(response, status=status.HTTP_200_OK)
  
  
