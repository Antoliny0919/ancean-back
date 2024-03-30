import pytest
from rest_framework import status
from conftest import package_http_request
from category.models import Category

@pytest.mark.parametrize(
  "is_finish",
  [
    pytest.param(False),
    pytest.param(True),
  ],
)
def test_relate_is_finish_state(post_client, is_finish):
  '''
  test the change in the post modification success resposne according to the is_finish field value
  '''
  created_post = post_client.user.post
  post_client.endpoint = f'/api/posts/{created_post.id}/'
  body = {
    'title': created_post.title, 
    'author': created_post.author.name, 
    'is_finish': is_finish
  }
  response = package_http_request(post_client, 'patch', body)
  assert response.status_code == status.HTTP_200_OK
  
  
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
  post_client.endpoint = f'/api/posts/{created_post.id}/'
  body = {
    'title': created_post.title, 
    'author': created_post.author.name, 
    'is_finish': is_finish, 
    'category': category.name
  }
  package_http_request(post_client, 'patch', body)
  category = Category.objects.get(name=category.name)
  assert category.post_count == expected_post_count

  