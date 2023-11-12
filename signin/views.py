from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ancean.settings.base import OAUTH_SECRETS_COLLECTION
from .oauth import Oauth

# Create your views here.

class LoadOAuthSigninView(APIView):
  
  def get(self, request, social):
    code = request.GET.get('code')
    secrets = OAUTH_SECRETS_COLLECTION[social.upper()]
    oauth = Oauth(secrets['CLIENT_ID'], secrets['CLIENT_SECRET'], social, code)
    oauth.set_access_token()
    user = oauth.get_user_info()
    print(user)
    return Response({'hello': '1234'}, status=status.HTTP_200_OK)
  

class LoadSigninView(APIView):
  
  def post(self, request):
    print(request.data)
    pass