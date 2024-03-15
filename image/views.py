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
    '''
    save the image requested  by the user
    path design --> '/ancean/media/{user_name}/{post_number(id)}/{file_name}'
    the id value of the post is required to save the image(it's mean image save only when post is created)
    '''
    name = request.user.name
    data = request.data
    id = data.get('id')
    image_file = data.get('file')
    user_image_store_path = f'{name}/{id}'
    save_path = os.path.join(getattr(settings, 'MEDIA_ROOT'), user_image_store_path)
    if not os.path.exists(save_path) or not id:
      return Response({'detail': '이미지를 생성할 수 없습니다. 먼저 포스트를 생성해주세요(임시저장).'}, status=status.HTTP_400_BAD_REQUEST)
    server = getattr(settings, 'SERVER_URI')
    with open(os.path.join(save_path, image_file.name), mode='wb') as file:
      for chunk in image_file.chunks():
        file.write(chunk)
    url = f'{server}/media/{name}/{id}/{image_file.name}'
    return Response({"success": 1, "file": {"url": url, "name": image_file.name}}, status=status.HTTP_200_OK)
