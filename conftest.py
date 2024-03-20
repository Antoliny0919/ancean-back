import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


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
}

# @pytest.fixture
# def django_db_setup():
#   from django.conf import settings

@pytest.fixture
def common_user(db):
  user = User.objects.create_user(**TEST_COMMON_USER_DATA)
  return user
  
@pytest.fixture
def admin_user(db):
  user = User.objects.create_superuser(**TEST_ADMIN_USER_DATA)
  return user
  

@pytest.fixture
def common_client(common_user):
  client = APIClient()
  client.user = common_user
  refresh = RefreshToken.for_user(common_user)
  access = str(refresh.access_token)
  client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
  return client

@pytest.fixture
def admin_client(admin_user):
  client = APIClient()
  refresh = RefreshToken.for_user(admin_user)
  access = str(refresh.access_token)
  client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
  return client
  
  
  