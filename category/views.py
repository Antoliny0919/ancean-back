import django_filters.rest_framework
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.filters import OrderingFilter
from .models import Category
from .serializer import CategorySerializer

# Create your views here.

class CategoryView(GenericAPIView, ListModelMixin):
  '''
  get categories in the order of many posters by category
  '''
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  filter_backends = [django_filters.rest_framework.DjangoFilterBackend, OrderingFilter]
  ordering_fields = ['post_count']
  
  def get(self, request, *args, **kwargs):
    return self.list(request)
