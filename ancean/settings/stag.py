import os
from .base import *

ALLOWED_HOSTS = ["*"]

# SECURITY WARNING: keep the secret key used in production secret!

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

POSTGRES_SECRETS_COLLECTION = get_secret(django_secrets, "POSTGRES")

SERVER_URI = f'http://ancean.stag'
  
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
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': POSTGRES_SECRETS_COLLECTION['POSTGRES_DATABASE_NAME'],
    'USER': POSTGRES_SECRETS_COLLECTION['POSTGRES_USER'],
    'PASSWORD': POSTGRES_SECRETS_COLLECTION['POSTGRES_PASSWORD'],
    'HOST': POSTGRES_SECRETS_COLLECTION['POSTGRES_HOST'],
    'PORT': POSTGRES_SECRETS_COLLECTION['POSTGRES_PORT'],
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
