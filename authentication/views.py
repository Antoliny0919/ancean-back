from rest_framework_simplejwt.views import TokenViewBase
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import CustomTokenObtainPairSerializer

# Create your views here.

def get_token_for_user(user):
  refresh = RefreshToken.for_user(user)
  
  return {
    'refresh': str(refresh),
    'access': str(refresh.access_token)
  }

class CustomTokenObtainPairView(TokenViewBase):
  serializer_class = CustomTokenObtainPairSerializer