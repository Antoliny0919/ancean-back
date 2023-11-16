from rest_framework.views import APIView
from rest_framework.response import Response
from ancean.settings.base import OAUTH_SECRETS_COLLECTION
from .oauth import Oauth
from authentication.views import get_token_for_user, set_token_response

class LoadOAuthSigninView(APIView):
  
  def get(self, request, social):
    code = request.GET.get('code')
    secrets = OAUTH_SECRETS_COLLECTION[social.upper()]
    oauth = Oauth(secrets['CLIENT_ID'], secrets['CLIENT_SECRET'], social, code)
    oauth.set_access_token()
    user_data = oauth.get_user_info()
    user = oauth.is_already_registered(user_data)
    if user:
      # is already registered user --> login-enabled status
      # get access, refresh token and set response header Set-Cookie 
      token = get_token_for_user(user)
      response = set_token_response(**token)
      return response
    else:
      # haven't registered yer user --> redirect signup
      return Response()
