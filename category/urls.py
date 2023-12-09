from django.urls import path
from . import views

urlpatterns = [
  path('category/', views.CategoryView.as_view(), name="get_all_category"),
  path('category/<str:category_name>/posts/', views.CategoryPostView.as_view(), name="get_category_post")
]
