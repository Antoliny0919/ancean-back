from conftest import package_http_request

def test_post(client, body):
  client.endpoint = '/api/post/'
  body['author'] = client.user.name
  response = package_http_request(client, 'post', body)
  
  print(response.data)

  assert 0
  
def test_posts(client, body):
  client.endpoint = '/api/posts/'
  body['author'] = client.user.name
  response = package_http_request(client, 'post', body)
  
  print(response.data)

  assert 0