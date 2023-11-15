from django.conf import settings
from django.http.response import HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from ancean.settings.base import OAUTH_SECRETS_COLLECTION
from .oauth import Oauth
from authentication.views import get_token_for_user

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
      token = get_token_for_user(user)
      return HttpResponseRedirect(redirect_to=settings.FRONT_URI)
    else:
      # haven't registered yer user --> redirect signup
      return Response()
