import os
import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from conftest import TEST_ADMIN_USER_DATA

User = get_user_model()

@pytest.mark.django_db
def test_personal_image_storage():
  '''
  test if a personal image storage is also created and removed when a user is created and removed
  '''
  created_user = User.objects.create_user(**TEST_ADMIN_USER_DATA)
  personal_image_storage_path = os.path.join(getattr(settings, 'MEDIA_ROOT'), f'{created_user.name}')
  assert os.path.exists(personal_image_storage_path)
  User.objects.delete_user(created_user)
  assert not os.path.exists(personal_image_storage_path)