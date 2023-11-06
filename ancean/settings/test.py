from .base import *

ALLOWED_HOSTS = ["*"]
DEBUG = False

CORS_ORIGIN_ALLOW_ALL = True

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': get_secret('POSTGRES_DATABASE_NAME'),
    'USER': get_secret('POSTGRES_USER'),
    'PASSWORD': get_secret('POSTGRES_PASSWORD'),
    'HOST': get_secret('POSTGRES_HOST'),
    'PORT': get_secret('POSTGRES_PORT'),
  }
}