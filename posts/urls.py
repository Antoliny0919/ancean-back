from django.urls import path, re_path
from . import views

urlpatterns = [
  path('posts/', views.PostView.as_view(), name="get_posts"),
  path('posts/<int:post_id>/', views.SinglePostView.as_view(), name="get_single_posts"),
  re_path('^posts/category/(?P<category_name>.+)/$', views.CategoryPostView.as_view(), name="get_category_post"),
]
