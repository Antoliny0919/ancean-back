from django.urls import path
from . import views

urlpatterns = [
  path('mail/code/', views.SendAuthcodeEmailView.as_view(), name="send_authcode_email"),
  path('user/', views.CreateUserView.as_view(), name="user")
]
