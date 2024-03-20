from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase, APIClient

# Create your tests here.

User = get_user_model()

class APICommonUserTest(APITestCase):
  
  common_tester = {'email': 'common_tester123@gmail.com', '_name': 'common_tester123', 'password': '12345678'}
  
  @classmethod
  def setUpTestData(cls):
    cls.client = APIClient()
    cls.user = User.objects.create_user(**cls.common_tester)
    refresh = RefreshToken.for_user(cls.user)
    access = str(refresh.access_token)
    cls.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
    
    
  def setUp(self):
    self.data = {
      'title': 'test post title',
      'author': f'{self.user.name}',
      'introduce': 'hello world!',
      'catogory': 'DOCKER',
      'is_finish': False,
    }
    
class APIAdminUserTest(APITestCase):
  
  admin_tester = {'email': 'admin_tester123@gmail.com', '_name': 'admin_tester123', 'password': '12345678', 'is_staff': True}
  
  @classmethod
  def setUpTestData(cls):
    cls.client = APIClient()
    cls.user = User.objects.create_user(**cls.admin_tester)
    refresh = RefreshToken.for_user(cls.user)
    access = str(refresh.access_token)
    cls.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
    
    
  def setUp(self):
    self.data = {
      'title': 'test post title',
      'author': f'{self.user.name}',
      'introduce': 'hello world!',
      'catogory': 'DOCKER',
      'is_finish': False,
    }
    
    