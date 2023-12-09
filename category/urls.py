from django.urls import path
from . import views

urlpatterns = [
  path('category/representative/', views.HomepageRepresentativeCategoryView.as_view(), name="get_representative7_category")
]
