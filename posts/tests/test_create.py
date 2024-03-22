import pytest
from django.urls import reverse
from rest_framework import status
from conftest import TEST_COMMON_USER_DATA, TEST_ADMIN_USER_DATA, TEST_POST_DATA
from posts.models import Post

@pytest.mark.parametrize(
"client, body, status_code",
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
indirect=['client']
)

def test_create_post(client, body, status_code):
  body['author'] = client.user.name
  response = client.post(reverse('posts_view'), body)
  assert response.status_code == status_code
  
def test_post(post):
  print(Post.objects.all())
  assert 0
  

# @pytest.mark.parametrize("client, body", [pytest.param(TEST_ADMIN_USER_DATA, TEST_POST_DATA)], indirect=["client"])
# def test_create_public_post(category, client, body):
#   body['author'], body['is_finish'] = client.user.name, True
#   client.post(reverse('posts_view'), body)
#   check_post = client.get(f'/api/posts/?id=1')
  
#   assert 0