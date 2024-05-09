import json
import os
from django.conf import settings
from rest_framework_simplejwt.views import (
  TokenViewBase,
  TokenRefreshView
)
from rest_framework_simplejwt.settings import api_settings


# Create your views here.

class CustomTokenViewBase(TokenViewBase):
  
  def finalize_response(self, request, response, *args, **kwargs):
    refresh_token = response.data['refresh']
    env = os.environ.get('DJANGO_SETTINGS_MODULE').split('.')[-1]
    if env == 'local':
      cookie_conf = {'httponly': False, 'secure': False, 'samesite': 'lax'}
    else :
      cookie_conf = {'domain': 'ancean.net', 'httponly': True, 'secure': True, 'samesite': 'lax'}

    exp = getattr(settings, 'SIMPLE_JWT')['REFRESH_TOKEN_LIFETIME']
    exp_millisec = exp.total_seconds()
    
    response.set_cookie(
      'refresh',
      refresh_token,
      **cookie_conf,
      max_age=exp_millisec
    )
    
    return super().finalize_response(request, response, *args, **kwargs)

class CustomTokenObtainPairView(CustomTokenViewBase):

  _serializer_class = api_settings.TOKEN_OBTAIN_SERIALIZER

class CustomTokenRefreshView(TokenRefreshView):
  
  def set_refresh_token(self):
    '''
    production server refresh token cookie have httponly attribute
    so data extraction by parsing the cookie part from the request header
    '''
    
    cookies_str = self.request.META["HTTP_COOKIE"]
    if "refresh" in cookies_str:
      cookies = {cookie.split("=")[0]: cookie.split("=")[1] for cookie in cookies_str.split("; ")}
      self.request.data["refresh"] = json.dumps(cookies["refresh"]).replace("\"", '')

  def post(self, request, *args, **kwargs):
    env = os.environ.get('DJANGO_SETTINGS_MODULE').split('.')[-1]
    if env != "local":
      self.set_refresh_token()
    
    return super().post(request, *args, **kwargs)
