from django.urls import path
from rest_framework_simplejwt.views import (
  TokenRefreshView,
)
from . import views


urlpatterns = [
  path('token/', views.CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
  path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
  path('mail/code/', views.SendAuthcodeEmailView.as_view(), name="send_authcode_email"),
]
