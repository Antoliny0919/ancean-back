from .base import *

ALLOWED_HOSTS = ["*"]
DEBUG = True

CORS_ORIGIN_ALLOW_ALL = True

SERVER_URI = 'http://localhost:5050'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# CACHES = {
#   "default": "django.core.cache.backends.memcached.PyMemcacheCache",
#   "LOCATION": [
#     "127.0.0.1:11211",
#   ]
# }