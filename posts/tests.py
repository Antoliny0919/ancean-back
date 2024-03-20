from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APITestCase, APIClient
from users.models import User

# Create your tests here.

class PostViewTest(APITestCase):
  
  common_tester = {'email': 'common_tester123@gmail.com', 'name': 'common_tester123', 'password': '12345678'}
  admin_tester = {}
  
  @classmethod
  def setUpTestData(cls):
    cls.client = APIClient()
    cls.endpoint = '/api/posts/'
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
  
  def test_user_create_post(self):
    response = self.__class__.client.post(self.endpoint, self.data, content_type="application/json")
    
    print(response.data)
  
    self.assertEqual(response.status_code, 201)
    
    # response = self.client.post(self.client.endpoint, data=self.data)
    
    # self.assertEqual(response.status_code, 403)
    
    
    
    
    
    