import json
from rest_framework import status
from category.models import Category

def test_patch_post(base_client, category):
  created_post = base_client.user.post
  body = {'title': created_post.title, 'author': created_post.author.name, 'is_finish': False}
  error_response = base_client.patch(base_client.endpoint, json.dumps(body), content_type='application/Json')
  assert error_response.status_code == status.HTTP_400_BAD_REQUEST
  assert error_response.data.get('detail') == '포스트 id를 확인할 수 없습니다.'
  
  body['id'] = created_post.id

  response = base_client.patch(base_client.endpoint, json.dumps(body), content_type='application/Json')
  
  assert response.status_code == status.HTTP_200_OK
  # category = Category.objects.get(name=category.name)
  # assert category.post_count == 0
  
  body['is_finish'] = True
  response = base_client.patch(base_client.endpoint, json.dumps(body), content_type='application/Json') 
  assert 0
  # category =Category.objects.get(name=category.name)

  # assert category.post_count == 1  