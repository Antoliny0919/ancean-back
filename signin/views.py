from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ancean.settings.base import OAUTH_SECRETS_COLLECTION
from .oauth import Oauth
from users.models import User

class LoadOAuthSigninView(APIView):
  
  def get(self, request, social):
    code = request.GET.get('code')
    secrets = OAUTH_SECRETS_COLLECTION[social.upper()]
    oauth = Oauth(secrets['CLIENT_ID'], secrets['CLIENT_SECRET'], social, code)
    oauth.set_access_token()
    user = oauth.get_user_info()
    is_registered = oauth.is_already_user(user)
    print(is_registered)
    return Response({'hello': '1234'}, status=status.HTTP_200_OK)
