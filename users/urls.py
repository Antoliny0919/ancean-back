from django.urls import path
from . import views

urlpatterns = [
  path('users/', views.TestView.as_view(), name="test_view")
]
