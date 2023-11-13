from rest_framework_simplejwt.views import TokenObtainPairView, TokenViewBase
from .serializers import CustomTokenObtainPairSerializer

# Create your views here.

class CustomTokenObtainPairView(TokenViewBase):
  serializer_class = CustomTokenObtainPairSerializer