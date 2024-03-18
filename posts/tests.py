from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase, APIClient
from users.models import User

# Create your tests here.

class PostViewTest(APITestCase):
  
  common_tester = {'email': 'common_tester123@gmail.com', 'name': 'common_tester123', 'password': '12345678'}
  
  @classmethod
  def setUpTestData(cls):
    cls.client = APIClient
    cls.endpoint = '/api/posts/'
    user = User.objects.create_user(**cls.common_tester)
    refresh = RefreshToken.for_user(user)
    cls.client.access = str(refresh.access_token)
    
    
    pass
    