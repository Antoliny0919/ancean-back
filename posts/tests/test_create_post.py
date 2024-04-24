import os
import pytest
from django.conf import settings
from rest_framework import status
from conftest import TEST_COMMON_USER_DATA, TEST_ADMIN_USER_DATA, package_http_request
from category.models import Category

@pytest.mark.parametrize(
"client, status_code",
[
  pytest.param({'user': TEST_COMMON_USER_DATA, 'endpoint': '/api/posts/'}, status.HTTP_403_FORBIDDEN),
  pytest.param({'user': TEST_ADMIN_USER_DATA, 'endpoint': '/api/posts/'}, status.HTTP_201_CREATED),
],
indirect=['client']
)

def test_relate_client(client, status_code, body):
  '''
  test post creation according to user
  only admin users can be post-created
  '''
  body['author'] = client.user.name
  response = package_http_request(client, 'post', body)
  assert response.status_code == status_code

@pytest.mark.parametrize(
"client, is_finish, post_count", 
[
  pytest.param({'user': TEST_ADMIN_USER_DATA, 'endpoint': '/api/posts/'}, True, 1),
  pytest.param({'user': TEST_ADMIN_USER_DATA, 'endpoint': '/api/posts/'}, False, 0),
],
indirect=["client"]
)
def test_relate_is_finish_state(category, client, is_finish, post_count, body):
  '''
  comparison of post generation difference according to is_finish status
  is_finish field is whether the post is finally issued or not
  '''
  body['author'], body['is_finish'], body['category'] = client.user.name, is_finish, category.name
  
  response = package_http_request(client, 'post', body)
  assert response.status_code == status.HTTP_201_CREATED
  post_id = response.data['id']
  check_post = package_http_request(client, 'get', url=f'/api/posts/{post_id}/')
  category = Category.objects.get(name=check_post.data['category'])
  
  assert category.post_count == post_count



@pytest.mark.parametrize("client", [pytest.param({'user': TEST_ADMIN_USER_DATA, 'endpoint': '/api/posts/'})], indirect=["client"])
def test_relate_image_storage(client, body):
  '''
  when a post is created, test whether a folder has been created to store the image file for the post
  '''
  body['author'] = client.user.name
  response = package_http_request(client, 'post', body)
  post_id = response.data['id']
  post_image_storage = os.path.join(getattr(settings, 'MEDIA_ROOT'), f'{client.user.name}/{post_id}')
  assert os.path.exists(post_image_storage)
  
@pytest.mark.parametrize("client, foreign_value, status_code",
[
  pytest.param({'user': TEST_ADMIN_USER_DATA, 'endpoint': '/api/posts/'}, {'category': 'NONE_EXIST_CATEGORY'}, status.HTTP_201_CREATED),
  pytest.param({'user': TEST_ADMIN_USER_DATA, 'endpoint': '/api/posts/'}, {'author': 'NONE_EXIST_USER'}, status.HTTP_400_BAD_REQUEST)
], indirect=["client"])
def test_relate_wrong_foreign_value(client, body, foreign_value, status_code):
  '''
  test foreign keys when client have request invalid(non-existent) values
  it the field is required, an error occurs, and the field that is not required is null
  '''
  body['author'] = client.user.name
  for key, value in foreign_value.items():
    body[key] = value

  response = package_http_request(client, 'post', body)
  
  assert response.status_code == status_code