from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'posts', views.PostViewSet, basename='post')

urlpatterns = [
  re_path('^posts/category/(?P<category_name>.+)/$', views.CategoryPostView.as_view(), name="get_category_post"),
]

urlpatterns += router.urls