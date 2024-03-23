import os
import pytest
import shutil
from django.conf import settings
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
  refresh = RefreshToken.for_user(user)
  access = str(refresh.access_token)
  client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
  
  yield client
  #teardown
  User.objects.delete_user(client.user)
  
@pytest.fixture()
def post(db):
  user = User.objects.create_user(**TEST_ADMIN_USER_DATA)
  TEST_POST_DATA['author'] = user
  Post.objects.create(**TEST_POST_DATA)

@pytest.fixture()
def category(db):
  Category.objects.create(name='DJANGO')
  