from django.urls import path
from . import views

urlpatterns = [
  path('posts/', views.PostView.as_view(), name="get_user_posts"),
  path('posts/test/', views.PostTestView.as_view(), name="test-view")
]
