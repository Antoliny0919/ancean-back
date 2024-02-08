import os
from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render

# Create your views here.

class ImageView(APIView):
  
  def post(self, request):
    data = request.data
    image_file = data.get('file')
    with open(os.path.join(getattr(settings, 'MEDIA_ROOT'), image_file.name), mode='wb') as file:
      for chunk in image_file.chunks():
        file.write(chunk)
    url = f'http://localhost:5050/media/{image_file.name}'
    return Response({"success": 1, "file": {"url": url, "name": image_file.name}}, status=status.HTTP_200_OK)
