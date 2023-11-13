from django.urls import path
from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView,
)
from . import views


urlpatterns = [
  path('oauth/<str:social>/', views.LoadOAuthSigninView.as_view(), name="load_oauth_signin"),
  # path('token/', TokenObtainPairView.as_view(), name="token_obtain_pair"),
  # path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
]
