from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ancean.settings.base import OAUTH_SECRETS_COLLECTION
from .oauth import Oauth
from authentication.views import get_token_for_user, login_success_response_jwt
  
    
class LoadOAuthSigninView(APIView):
  
  def get(self, request):
    code = request.GET.get('code')
    social = request.GET.get('social')
    secrets = OAUTH_SECRETS_COLLECTION[social.upper()]
    oauth = Oauth(secrets['CLIENT_ID'], secrets['CLIENT_SECRET'], social, code)
    oauth.set_access_token()
    user_data = oauth.get_user_info()
    user = oauth.is_already_registered(user_data)
    if user['registered']:
      # is already registered user --> login-enabled status
      token = get_token_for_user(user['user'])
      response = login_success_response_jwt(user['user'], token)

      return response
    else:
      # haven't registered yer user --> redirect signup
      return Response(user, status=status.HTTP_200_OK)
