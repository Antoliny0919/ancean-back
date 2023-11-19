from django.urls import path
from . import views


urlpatterns = [
  path('oauth/', views.LoadOAuthSigninView.as_view(), name="load_oauth_signin"),
]
