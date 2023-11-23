from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserModelSerializer

# Create your views here.

class TestView(APIView):
  
  def get(self, request):
    user = User.objects.all()
    serializer = UserModelSerializer(user, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)