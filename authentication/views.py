import time
import jwt
from django.conf import settings
from django.http.response import HttpResponseRedirect
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .serializers import CustomTokenObtainPairSerializer

# Create your views here.

def get_token_for_user(user):
  refresh = RefreshToken.for_user(user)
  
  return {
    'refresh': str(refresh),
    'access': str(refresh.access_token)
  }
  
def set_token_response(**kwargs) -> HttpResponseRedirect:
  '''
  setting access, refresh token Response header Set-Cookie 
  '''
  response = HttpResponseRedirect(redirect_to=settings.FRONT_URI)
  for name, value in kwargs.items():
    # decode jwt token cause get 'exp' data
    payload = jwt.decode(value, key=settings.SECRET_KEY, algorithms='HS256')
    # 'exp' timestamp - current time timestamp + 9hours(convert UTC to korea time)
    max_age = payload['exp'] - time.time() + (60 * 60 * 9)
    if settings.FRONT_URI.split(':')[0] == 'https':
      response.set_cookie(name, value, max_age=max_age, httponly=True, secure=True)
    else:
      response.set_cookie(name, value, max_age=max_age)

  return response


class CustomTokenViewBase(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = None
    _serializer_class = ""

    www_authenticate_realm = "api"

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        response = set_token_response(**serializer.validated_data)
        return response


class CustomTokenObtainPairView(CustomTokenViewBase):
  serializer_class = CustomTokenObtainPairSerializer