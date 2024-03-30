# import copy
# import time
# import random
# import pytest
# from django.core.cache import cache
# from posts.models import Post
# from users.models import User
# from category.models import Category
# from conftest import package_http_request, set_client, TEST_POST_DATA, TEST_ADMIN_USER2_DATA

# CATEGORIES_NAME = ['DJANGO', 'DOCKER', 'GOLANG']

# @pytest.fixture(scope='module')
# def categories(django_db_blocker):
#   with django_db_blocker.unblock():
#     categories = [Category.objects.create(name=category) for category in CATEGORIES_NAME]
  
#   return categories

# @pytest.fixture(scope='module')
# def client_and_posts(categories, django_db_blocker):
#   with django_db_blocker.unblock():
#     default_body = copy.deepcopy(TEST_POST_DATA)
#     user = User.objects.create_user(**TEST_ADMIN_USER2_DATA)
#     client = set_client(user, '/api/posts/')
#     default_body['author'] = client.user.name
    
#     for i in range(10000):
#       body = copy.deepcopy(default_body)
#       body['title'] = f'{body["title"]}-{i}'
#       package_http_request(client, 'post', body)
    
#     yield client
    

# @pytest.mark.parametrize(
#   'query',
#   [pytest.param(''), pytest.param('id=1'), pytest.param('category=DJANGO')]
# )
# def test_post_get_query(client_and_posts, query):
#   client = client_and_posts
#   if query:
#     url = f'{client.endpoint}?{query}'
#     response = package_http_request(client, 'get', url=url)
#   else:
#     response = package_http_request(client, 'get')
#   print(response.data)
    
  
#   assert 0