from rest_framework import views, status
from rest_framework.response import Response
from .serializers import UserModelSerializer

# Create your views here.

class UserView(views.APIView):
  
  def get(self, request):
    '''
    get data about users authenticated through tokens.
    '''
    
    serializer = UserModelSerializer(request.user)
    
    return Response(serializer.data, status=status.HTTP_200_OK)