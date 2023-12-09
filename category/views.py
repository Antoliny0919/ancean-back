from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category
from .serializer import CategorySerializer

# Create your views here.

class HomepageRepresentativeCategoryView(APIView):
  
  def get(self, request):
    RepresentativeCategory = Category.objects.all().order_by('-post_count')[:7]
    serializer = CategorySerializer(RepresentativeCategory, many=True)
    return Response(serializer.data, status.HTTP_200_OK)