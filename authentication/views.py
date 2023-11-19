import jwt
from django.conf import settings
from rest_framework import status, generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from .serializers import CustomTokenObtainPairSerializer
from users.serializers import UserSerializer

# Create your views here.

def get_token_for_user(user):
  refresh = RefreshToken.for_user(user)
  
  return {
    'refresh': str(refresh),
    'access': str(refresh.access_token)
  }

def get_expire(token_value):
  payload = jwt.decode(token_value, key=settings.SECRET_KEY, algorithms='HS256')
  return payload['exp']

def login_success_response_jwt(user, token):
  
  user = UserSerializer(user)
  token_data = {name: {'value': value, 'exp': get_expire(value)} for name, value in token.items()}
  data = {'token': token_data, 'user': user.data}
  
  return Response(data, status=status.HTTP_200_OK)


class CustomTokenViewBase(generics.GenericAPIView):
    permission_classes = ()
    authentication_classes = ()

    serializer_class = None
    _serializer_class = ""

    www_authenticate_realm = "api"

    def post(self, request: Request) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        
        user = serializer.validated_data['user']
        token = {name: value for name, value in serializer.validated_data.items() if name in ['access', 'refresh']}
        response = login_success_response_jwt(user, token)
        
        return response


class CustomTokenObtainPairView(CustomTokenViewBase):
  serializer_class = CustomTokenObtainPairSerializer
  
  