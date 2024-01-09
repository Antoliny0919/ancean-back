from django.urls import path
from . import views

urlpatterns = [
  path('uploadImage/', views.ImageView.as_view(), name="image-view"),
]
