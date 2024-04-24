import os
from .base import *

ALLOWED_HOSTS = ["*"]
DEBUG = False

CORS_ORIGIN_ALLOW_ALL = True

POSTGRES_SECRETS = os.path.join(SECRETS_FOLDER, 'postgres-secrets.json')

SERVER_URI = 'http://localhost:80'

with open(POSTGRES_SECRETS) as f:
  postgres_secrets = json.loads(f.read())

  
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
    'NAME': get_secret(postgres_secrets, 'POSTGRES_DATABASE_NAME'),
    'USER': get_secret(postgres_secrets, 'POSTGRES_USER'),
    'PASSWORD': get_secret(postgres_secrets, 'POSTGRES_PASSWORD'),
    'HOST': get_secret(postgres_secrets, 'POSTGRES_HOST'),
    'PORT': get_secret(postgres_secrets, 'POSTGRES_PORT'),
  }
}


# CACHES = {
#   "default": {
#     "BACKEND": "django_redis.cache.RedisCache",
#     "LOCATION": "redis://ancean-redis-service:6379/1",
#     "OPTIONS": {
#         "CLIENT_CLASS": "django_redis.client.DefaultClient",
#     }
#   }
# }