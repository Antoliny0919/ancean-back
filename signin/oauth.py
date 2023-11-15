import requests
from users.models import User

class Oauth:
  redirect_uri = 'http://localhost:5050/api/oauth'
  grant_type = 'authorization_code'

  oauth_key = {
    'google': {
      'headers': {
        'Content-type': 'application/x-www-form-urlencoded'
      },
      'api': {
        'get_token': 'https://oauth2.googleapis.com/token',
        'get_userinfo': 'https://www.googleapis.com/oauth2/v2/userinfo'
      },
      'get_email': ['email']
    },
    'github': {
      'headers': {
        'accept': 'application/json'
      },
      'api': {
        'get_token': 'https://github.com/login/oauth/access_token',
        'get_userinfo': 'https://api.github.com/user'
      },
      'get_email': ['email']
    },
    'kakao': {
      'headers': {
        'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'
      },
      'api': {
        'get_token': 'https://kauth.kakao.com/oauth/token',
        'get_userinfo': 'https://kapi.kakao.com/v2/user/me'
      },
      'get_email': ['kakao_account', 'email']
    }
  }
  
  def __init__(self, client_id, client_secret, social, code):
    self._client_id = client_id
    self._client_secret = client_secret
    self._social = social
    self._oauth_api = Oauth.oauth_key[social]['api']
    self._code = code
    
  def set_access_token(self):
    '''
    get access_token and save --> use oauth_api
    '''
    headers = Oauth.oauth_key[self._social]['headers']
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
    '''
    access_token is requried to execute this method
    if have access_token, get user information through it.
    '''
    
    if not hasattr(self, 'access_token'):
      raise 'access_token is required to obtain user information. \
        use "set_access_token" method first to acquire and save the token'
    
    user = requests.get(self._oauth_api['get_userinfo'], headers={
      'Authorization': f'{self.token_type} {self.access_token}'
    }).json()
    
    return user
  
  def is_already_registered(self, oauth_user_data):
    '''
    get email value from the oauth_user_data dictionary
    check by oauth email data is already registered(user) user 
    '''
    get_email = Oauth.oauth_key[self._social]['get_email']
    email = oauth_user_data
    
    for i in get_email:
      try:
        email = email[i]
      except KeyError:
        raise 'invalid attribute collection get_email for accessing email from the object'
    self._oauth_email = email
    
    try:
      user = User.objects.get(email=self._oauth_email)
      return user
      # if client haven't registered yet, redirect sign up page
    except User.DoesNotExist:
      return False