import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
  "body,status_code",
  [
    pytest.param(
      { 
        'title': 'test post title', 
        'introduce': 'hello world!',
        'catogory': 'DOCKER',
        'is_finish': False,
      },
      status.HTTP_201_CREATED
    )
  ]
)



def test_create_post(common_client, body, status_code):
  body['author'] = common_client.user.name
  response = common_client.post(reverse('get_posts'), body)
  
  assert response.status_code == status_code
