import requests

class Oauth:
  redirect_uri = 'http://localhost:5050/api/oauth'
  grant_type = 'authorization_code'

  oauth_data = {
    'google': {
      'headers': {
        'Content-type': 'application/x-www-form-urlencoded'
      },
      'api': {
        'get_token': 'https://oauth2.googleapis.com/token',
        'get_userinfo': 'https://www.googleapis.com/oauth2/v2/userinfo'
      }
    },
    'github': {
      'headers': {
        'accept': 'application/json'
      },
      'api': {
        'get_token': 'https://github.com/login/oauth/access_token',
        'get_userinfo': 'https://api.github.com/user'
      }
    },
    'kakao': {
      'headers': {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
      },
      'api': {
        'get_token': 'https://kauth.kakao.com/oauth/token',
        'get_userinfo': 'https://kapi.kakao.com/v2/user/me'
      }
    }
  }
  
  def __init__(self, client_id, client_secret, social, code):
    self._client_id = client_id
    self._client_secret = client_secret
    self._social = social
    self._oauth_api = Oauth.oauth_data[social]['api']
    self._code = code
    
  def set_access_token(self):
    headers = Oauth.oauth_data[self._social]['headers']
    body = {
      'client_id': self._client_id,
      'client_secret': self._client_secret,
      'code': self._code,
      'redirect_uri': f'{Oauth.redirect_uri}/{self._social}',
      'grant_type': Oauth.grant_type
    }
    
    token = requests.post(self._oauth_api['get_token'], headers=headers, data=body).json()
    self.access_token = token['access_token']
    self.token_type = token['token_type']
    
  def get_user_info(self):
    # must obtain access_token before importing user information
    if not hasattr(self, 'access_token'):
      raise 'access_token is required to obtain user information.'
    
    user = requests.get(self._oauth_api['get_userinfo'], headers={
      'Authorization': f'{self.token_type} {self.access_token}'
    }).json()
    
    return user