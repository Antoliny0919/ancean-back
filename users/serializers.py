from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
from .validators import FormatValidator


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('email', 'introduce')
    
class DuplicateEmailSerializer(serializers.Serializer):
  
  email = serializers.EmailField(validators=[
    FormatValidator('유효한 이메일 형식이 아닙니다.', r'[a-z0-9_]+@[a-z]+\.[a-z]{2,3}'),
    UniqueValidator(queryset=User.objects.all(), message='이미 존재하는 이메일입니다.')
  ])