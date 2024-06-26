import os
import pytest
from django.conf import settings
from rest_framework import status
from category.models import Category
from conftest import TEST_ADMIN_USER_DATA, TEST_ADMIN_USER2_DATA, package_http_request

  
@pytest.mark.parametrize('clients', [pytest.param({'user': [TEST_ADMIN_USER_DATA, TEST_ADMIN_USER2_DATA], 'endpoint': '/api/posts/'})], indirect=['clients'])
def test_not_owner_request(clients, body):
  '''
  post cannot be delete by users other than the owner of post
  test when a user other than the owner of the post tries to delete the post
  '''
  client_a, client_b = clients[0], clients[1]
  body['author'] = client_a.user.name
  created_post = package_http_request(client_a, 'post', body=body)
  created_post_id = created_post.data['id']
  client_b.endpoint = f'/api/posts/{created_post_id}/'
  error_response = package_http_request(client_b, 'delete')
   
  assert error_response.status_code == status.HTTP_403_FORBIDDEN
  assert error_response.data == {'detail': '해당 포스트에 대한 권한이 존재하지 않습니다.'}
  

@pytest.mark.parametrize(
  'post_client, expected_before_post_count, expected_after_post_count', 
  [
    pytest.param({'is_finish': True, 'category': 'DJANGO'}, 1, 0),
    pytest.param({'is_finish': False, 'category': 'DJANGO'}, 0, 0),
  ], indirect=['post_client'])
def test_relate_category(post_client, expected_before_post_count, expected_after_post_count):
  '''
  observe changes in properties of category objects associated with posts due to post delete
  '''
  created_post = post_client.user.post
  before_category = Category.objects.get(name=created_post.category.name)
  assert before_category.post_count == expected_before_post_count
  post_client.endpoint = f'/api/posts/{created_post.id}/'
  response = package_http_request(post_client, 'delete')
  after_category = Category.objects.get(name=created_post.category.name)
  assert response.status_code == status.HTTP_204_NO_CONTENT
  assert after_category.post_count == expected_after_post_count
  
def test_relate_image_storage(post_client):
  '''
  post deletion require the image storage of that post to also be deleted
  '''
  created_post = post_client.user.post
  post_client.endpoint = f'/api/posts/{created_post.id}/'
  package_http_request(post_client, 'delete')
  post_image_storage_path = os.path.join(getattr(settings, 'MEDIA_ROOT'), f'{post_client.user.name}/{created_post.id}')
  
  assert os.path.exists(post_image_storage_path) == False