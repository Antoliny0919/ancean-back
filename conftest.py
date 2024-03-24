import copy
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from category.models import Category
from posts.models import Post


User = get_user_model()

TEST_COMMON_USER_DATA = {
  'email': 'common_tester123@gmail.com', 
  '_name': 'common_tester123', 
  'password': '12345678'
}

TEST_ADMIN_USER_DATA = {
  'email': 'admin_tester123@gmail.com', 
  '_name': 'admin_tester123', 
  'password': '12345678', 
  'is_staff': True,
  'is_superuser': True,
}

TEST_POST_DATA = {
  'title': 'test post title', 
  'introduce': 'hello world!',
  'is_finish': False,
}
  
@pytest.fixture()
def client(request, db):
  user_data = request.param
  user = User.objects.create_user(**user_data)
  client = APIClient()
  client.user = user
  client.endpoint = '/api/posts/'
  refresh = RefreshToken.for_user(user)
  access = str(refresh.access_token)
  client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
  
  yield client
  #teardown
  User.objects.delete_user(client.user)
  
@pytest.fixture()
def base_client(body, db):
  '''
  
  '''
  user = User.objects.create_user(**TEST_ADMIN_USER_DATA)
  client = APIClient()
  client.user = user
  client.endpoint = '/api/posts/'
  refresh = RefreshToken.for_user(user)
  access = str(refresh.access_token)
  client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
  
  body['author'] = client.user.name
  create_post = client.post(client.endpoint, body)
  created_post = Post.objects.get(id=create_post.data['id'])
  client.user.post = created_post
  
  yield client
  
  User.objects.delete_user(client.user)
  

@pytest.fixture()
def category(db):
  category = Category.objects.create(name='DJANGO')
  return category

@pytest.fixture()
def body():
  body = copy.deepcopy(TEST_POST_DATA)
  return body
