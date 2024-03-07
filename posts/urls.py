from django.urls import path, re_path
from . import views

urlpatterns = [
  path('posts/', views.PostView.as_view(), name="get_posts"),
  path('posts/test/', views.TestPostView.as_view(), name="get_posts_test"),
  re_path('^posts/category/(?P<category_name>.+)/$', views.CategoryPostView.as_view(), name="get_category_post"),
]
