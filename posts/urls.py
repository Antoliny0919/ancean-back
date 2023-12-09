from django.urls import path
from . import views

urlpatterns = [
  path('<str:name>/posts/', views.PostView.as_view(), name="get_user_posts"),
]
