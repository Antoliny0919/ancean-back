import pytest
from django.urls import reverse
from rest_framework import status
from conftest import TEST_COMMON_USER_DATA, TEST_ADMIN_USER_DATA
from category.models import Category

def expected_is_finish_response(id):
  return {'redirect_path': f'/posts/{id}/', 'id': id}

def expected_none_is_finish_response(id):
  return {'detail': '포스트가 생성되었습니다.', 'id': id}

@pytest.mark.parametrize(
"client, status_code",
[
  pytest.param(TEST_COMMON_USER_DATA, status.HTTP_403_FORBIDDEN),
  pytest.param(TEST_ADMIN_USER_DATA, status.HTTP_201_CREATED),
],
indirect=['client']
)

def test_user_create_post(client, status_code, body):
  '''
  test post creation according to user
  only admin users can be post-created
  '''
  body['author'] = client.user.name
  response = client.post(reverse('posts_view'), body)
  assert response.status_code == status_code
    

@pytest.mark.parametrize(
"client, is_finish, expected_response, post_count", 
[
  pytest.param(TEST_ADMIN_USER_DATA, True, expected_is_finish_response, 1),
  pytest.param(TEST_ADMIN_USER_DATA, False, expected_none_is_finish_response, 0)
],
indirect=["client"]
)
def test_is_finish_create_post(category, client, is_finish, expected_response, post_count, body):
  '''
  comparison of post generation difference according to is_finish status
  is_finish field is whether the post is finally issued or not
  '''
  body['author'], body['is_finish'], body['category'] = client.user.name, is_finish, category.name
  
  response = client.post(reverse('posts_view'), body)
  assert response.status_code == status.HTTP_201_CREATED
  post_id = response.data['id']
  assert response.data == expected_response(post_id)
  check_post = client.get(f'/api/posts/?id={post_id}')
  category = Category.objects.get(name=check_post.data['category'])
  
  assert category.post_count == post_count
  
  