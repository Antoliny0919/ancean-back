import os
from .base import *

ALLOWED_HOSTS = ["*"]

# SECURITY WARNING: keep the secret key used in production secret!

DEBUG = True

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

SERVER_URI = f'http://ancean.stag'

MYSQL_SECRETS_COLLECTION = get_secret(django_secrets, "MYSQL")
  
MIDDLEWARE = [
  'django_prometheus.middleware.PrometheusBeforeMiddleware',
  'corsheaders.middleware.CorsMiddleware',
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
  'django_prometheus.middleware.PrometheusAfterMiddleware',
]

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': MYSQL_SECRETS_COLLECTION['MYSQL_DATABASE_NAME'],
    'USER': MYSQL_SECRETS_COLLECTION['MYSQL_USER'],
    'PASSWORD': MYSQL_SECRETS_COLLECTION['MYSQL_PASSWORD'],
    'HOST': MYSQL_SECRETS_COLLECTION['MYSQL_HOST'],
    'PORT': MYSQL_SECRETS_COLLECTION['MYSQL_PORT'],
  }
}

# CACHES = {
#   "default": {
#     "BACKEND": "django_redis.cache.RedisCache",
#     "LOCATION": f"redis://ancean-stag_redis:6379/1",
#     "OPTIONS": {
#         "CLIENT_CLASS": "django_redis.client.DefaultClient",
#     }
#   }
# }
