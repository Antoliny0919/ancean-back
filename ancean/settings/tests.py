import os
from django.contrib import admin
from django.urls import path, include
# from settings.base import BASE_DIR

# APP_LIST = [dir for dir in os.listdir(BASE_DIR) if dir.find(".") == -1].remove("ancean")


# URL_PATTERNS = [path('api/', include(f'{app}.urls')) for app in APP_LIST].append(path('admin/', admin.site.urls))


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    # path('api/', include('signin.urls')),
]