from rest_framework import serializers
from users.models import User
  
class UserModelSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = User
    fields = ('email', 'name', 'introduce', 'is_staff')
    