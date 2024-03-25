import os
import json
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

def test_user_create_post(client, status_code, body):
  '''
  test post creation according to user
  only admin users can be post-created
  '''
  body['author'] = client.user.name
  response = package_http_request(client, 'post', body)
  assert response.status_code == status_code

@pytest.mark.parametrize(
"client, is_finish, expected_response, post_count", 
[
  pytest.param({'user': TEST_ADMIN_USER_DATA, 'endpoint': '/api/posts/'}, True, lambda id: {'redirect_path': f'/posts/{id}/', 'id': id}, 1),
  pytest.param({'user': TEST_ADMIN_USER_DATA, 'endpoint': '/api/posts/'}, False, lambda id: {'detail': '포스트가 생성되었습니다.', 'id': id}, 0)
],
indirect=["client"]
)
def test_is_finish_create_post(category, client, is_finish, expected_response, post_count, body):
  '''
  comparison of post generation difference according to is_finish status
  is_finish field is whether the post is finally issued or not
  '''
  body['author'], body['is_finish'], body['category'] = client.user.name, is_finish, category.name
  
  response = package_http_request(client, 'post', body)
  assert response.status_code == status.HTTP_201_CREATED
  post_id = response.data['id']
  assert response.data == expected_response(post_id)
  check_post = package_http_request(client, 'get', url=f'/api/posts/?id={post_id}')
  category = Category.objects.get(name=check_post.data['category'])
  
  assert category.post_count == post_count


@pytest.mark.parametrize("client", [pytest.param({'user': TEST_ADMIN_USER_DATA, 'endpoint': '/api/posts/'})], indirect=["client"])
def test_image_storage_create_post(client, body):
  '''
  when a post is created, test whether a folder has been created to store the image file for the post
  '''
  body['author'] = client.user.name
  response = package_http_request(client, 'post', body)
  post_id = response.data['id']
  post_image_storage = os.path.join(getattr(settings, 'MEDIA_ROOT'), f'{client.user.name}/{post_id}')
  assert os.path.exists(post_image_storage)
  
  
  