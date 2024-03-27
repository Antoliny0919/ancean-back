import pytest
from rest_framework import status
from conftest import package_http_request
from category.models import Category

def test_wrong_request(post_client):
  '''
  post modification identifies the post to be corrected through the post id value of the request
  this test when client did not send id case
  '''
  created_post = post_client.user.post
  body = {'title': created_post.title, 'author': created_post.author.name, 'is_finish': False}
  error_response = package_http_request(post_client, 'patch', body)
  assert error_response.status_code == status.HTTP_400_BAD_REQUEST
  assert error_response.data == {'detail': '포스트 id를 확인할 수 없습니다.'}


@pytest.mark.parametrize(
  "is_finish, expected_response",
  [
    pytest.param(False, {'detail': '포스트가 임시저장되었습니다.'}),
    pytest.param(True, {'redirect_path': '/posts/1/'})
  ],
)
def test_relate_is_finish_state(post_client, is_finish, expected_response):
  '''
  test the change in the post modification success resposne according to the is_finish field value
  '''
  created_post = post_client.user.post
  body = {
    'id': created_post.id, 
    'title': created_post.title, 
    'author': created_post.author.name, 
    'is_finish': is_finish
  }
  response = package_http_request(post_client, 'patch', body)
  assert response.status_code == status.HTTP_200_OK
  assert response.data == expected_response
  
  
@pytest.mark.parametrize(
  "is_finish, expected_post_count",
  [
    pytest.param(True, 1),
    pytest.param(False, 0)
  ],
)
def test_relate_category(category, post_client, is_finish, expected_post_count):
  '''
  when a post have a category
  test the change in the post_count field value of the foreign key category
  according to the is_finish field value
  '''
  created_post =  post_client.user.post
  body = {
    'id': created_post.id, 
    'title': created_post.title, 
    'author': created_post.author.name, 
    'is_finish': is_finish, 
    'category': category.name
  }
  package_http_request(post_client, 'patch', body)
  category = Category.objects.get(name=category.name)
  assert category.post_count == expected_post_count

  