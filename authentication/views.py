from rest_framework_simplejwt.views import TokenViewBase
from .serializers import CustomTokenObtainPairSerializer

# Create your views here.

class CustomTokenObtainPairView(TokenViewBase):
  serializer_class = CustomTokenObtainPairSerializer