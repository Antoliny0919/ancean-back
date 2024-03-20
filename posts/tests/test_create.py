import pytest
from django.urls import reverse
from rest_framework import status
from conftest import TEST_COMMON_USER_DATA, TEST_ADMIN_USER_DATA, TEST_POST_DATA


@pytest.mark.parametrize(
"client,body,status_code",
[
  pytest.param(
    TEST_COMMON_USER_DATA,
    TEST_POST_DATA,
    status.HTTP_403_FORBIDDEN
  ),
  pytest.param(
    TEST_ADMIN_USER_DATA,
    TEST_POST_DATA,
    status.HTTP_201_CREATED
  ),
],
indirect=["client"]
)

def test_client(client, body, status_code):
  
  body['author'] = client.user.name
  response = client.post(reverse('get_posts'), body)
  assert response.status_code == status_code
