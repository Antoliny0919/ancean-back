import os
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

# Create your views here.

class ImageView(APIView):
  
  permission_classes = [IsAdminUser]
  
  def post(self, request):
    name = request.user.name
    data = request.data
    id = data.get('id')
    image_file = data.get('file')
    user_image_store_path = f'{name}/{id}'
    save_path = os.path.join(getattr(settings, 'MEDIA_ROOT'), user_image_store_path)
    if not os.path.exists(save_path) or not id:
      return Response({'hellowrold': 'fail'}, status=status.HTTP_400_BAD_REQUEST)
    server = getattr(settings, 'SERVER_URI')
    with open(os.path.join(save_path, f'/{image_file.name}'), mode='wb') as file:
      for chunk in image_file.chunks():
        file.write(chunk)
    url = f'{server}/media/{image_file.name}'
    return Response({"success": 1, "file": {"url": url, "name": image_file.name}}, status=status.HTTP_200_OK)
