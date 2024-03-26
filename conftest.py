import os
import json
import copy
import pytest
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

TEST_ADMIN_USER2_DATA= {
  'email': 'admin_tester1234@gmail.com',
  '_name': 'admin_tester1234',
  'password': '12345678',
  'is_staff': True,
  'is_superuser': True,
}

TEST_POST_DATA = {
  'title': 'test post title', 
  'introduce': 'hello world!',
  'is_finish': False,
}

def pytest_report_header(config):
  return f"ancean api test -> env: {os.environ['DJANGO_SETTINGS_MODULE']}"

def set_client(user, endpoint):
  '''
  set client object default settings
  '''
  client = APIClient()
  client.user = user
  client.endpoint = endpoint
  refresh = RefreshToken.for_user(user)
  access = str(refresh.access_token)
  client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
  
  return client

def package_http_request(client, method, body=None, url=None):
  '''
  default setting of HTTP request for API client object
  '''
  request_http_method = getattr(client, method.lower())
  if not url:
    url = client.endpoint
  
  if body:
    response = request_http_method(url, json.dumps(body), content_type='application/Json')
    return response
  
  response = request_http_method(url)
  return response
  
@pytest.fixture(params=[{'user': TEST_ADMIN_USER_DATA, 'endpoint': '/'}])
def client(request, db):
  user_data = request.param['user']
  user = User.objects.create_user(**user_data)
  client = set_client(user, request.param['endpoint'])
  
  yield client
  #teardown
  User.objects.delete_user(client.user)
  
@pytest.fixture(params=[{'user': [TEST_ADMIN_USER_DATA], 'endpoint': '/'}])
def clients(request, db):
  '''
  user parameters can receive multiple user data in array form
  fixture to create multiple user
  '''
  clients = []
  users_data = request.param['user']
  for user_data in users_data:
    user = User.objects.create_user(**user_data)
    client = set_client(user, request.param['endpoint'])
    clients.append(client)
    
  yield clients
  
  for client in clients:
    User.objects.delete_user(client.user)
  
@pytest.fixture(params=[{'is_finish': False, 'category': ''}])
def post_client(request, client, category, body, db):
  '''
  create a dedicated client for post related testing
  '''
  client.endpoint = '/api/posts/'
  body['author'] = client.user.name
  body['category'], body['is_finish'] = request.param.get('category', ''), request.param.get('is_finish', False)
  create_post = client.post(client.endpoint, body)
  created_post = Post.objects.get(id=create_post.data['id'])
  client.user.post = created_post
  
  yield client

@pytest.fixture()
def category(db):
  category = Category.objects.create(name='DJANGO')
  return category

@pytest.fixture()
def body():
  body = copy.deepcopy(TEST_POST_DATA)
  return body
