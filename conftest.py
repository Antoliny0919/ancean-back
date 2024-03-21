import os
import pytest
import shutil
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from category.models import Category


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
  'category': 'DJANGO',
  'is_finish': False,
}

TEST_DB = {
  'ENGINE': 'django.db.backends.sqlite3',
  'NAME': os.path.join(getattr(settings, 'BASE_DIR'), 'testdb.sqlite3'),
}

@pytest.fixture()
def django_db_setup():
  settings.DATABASES['default']['test'] = TEST_DB

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
  personal_image_storage = os.path.join(getattr(settings, 'MEDIA_ROOT'), f'{client.user.name}')
  shutil.rmtree(personal_image_storage, ignore_errors=True)
  

@pytest.fixture()
def category(db):
  category = Category.objects.create(name='DJANGO')
  return category
  