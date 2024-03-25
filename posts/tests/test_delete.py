import os
import json
import pytest
from django.conf import settings
from rest_framework import status
from category.models import Category
from conftest import TEST_ADMIN_USER_DATA, TEST_ADMIN_USER2_DATA


def test_non_id_delete_post(post_client):
  error_response = post_client.delete(post_client.endpoint)
  
  assert error_response.status_code == status.HTTP_400_BAD_REQUEST
  assert error_response.data == {'detail': '포스트 id를 확인할 수 없습니다.'}
  
@pytest.mark.parametrize('clients', [pytest.param({'user': [TEST_ADMIN_USER_DATA, TEST_ADMIN_USER2_DATA], 'endpoint': '/api/posts/'})], indirect=['clients'])
def test_not_owner_delete_post(clients, body):
  
  client_a, client_b = clients[0], clients[1]
  body['author'] = client_a.user.name
  created_post = client_a.post(client_a.endpoint, json.dumps(body), content_type='application/Json')
  created_post_id = created_post.data['id']
  error_response = client_b.delete(client_b.endpoint, json.dumps({'id': created_post_id}), content_type='application/Json')
   
  assert error_response.status_code == status.HTTP_403_FORBIDDEN
  assert error_response.data == {'detail': '해당 포스트에 대한 권한이 존재하지 않습니다.'}
  

@pytest.mark.parametrize(
  'post_client, expected_before_post_count, expected_after_post_count', 
  [
    pytest.param({'is_finish': True, 'category': 'DJANGO'}, 1, 0),
    pytest.param({'is_finish': False, 'category': 'DJANGO'}, 0, 0),
  ], indirect=['post_client'])
def test_category_delete_post(post_client, expected_before_post_count, expected_after_post_count):
  
  created_post = post_client.user.post
  before_category = Category.objects.get(name=created_post.category.name)
  assert before_category.post_count == expected_before_post_count
  response = post_client.delete(post_client.endpoint, json.dumps({'id': created_post.id}), content_type='application/Json')
  after_category = Category.objects.get(name=created_post.category.name)
  assert response.status_code == status.HTTP_204_NO_CONTENT
  assert after_category.post_count == expected_after_post_count
  
def test_image_storage_delete_post(post_client):
  created_post = post_client.user.post
  post_client.delete(post_client.endpoint, json.dumps({'id': created_post.id}), content_type='application/Json')
  post_image_storage_path = os.path.join(getattr(settings, 'MEDIA_ROOT'), f'{post_client.user.name}/{created_post.id}')
  
  assert os.path.exists(post_image_storage_path) == False