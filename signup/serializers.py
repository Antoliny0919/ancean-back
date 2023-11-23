from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueValidator
from users.models import User
from .validators import FormatValidator

class UserValidationSerializer(serializers.Serializer):
  
  email = serializers.EmailField()
  password1 = serializers.CharField(validators=[
    FormatValidator('비밀번호는 8자 이상이며 영문 소문자와 특수문자를 최소 한개씩 포함해야합니다.',
    r'^(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$'
  )])
  password2 = serializers.CharField()
  introduce = serializers.CharField()

  def validate_introduce(self, introduce):
    if len(introduce) > 10:
      raise ValidationError('자기소개는 10자 이하로 해줘')
    return introduce
  
  def validate(self, data):
    password = data['password1']
    password_check = data['password2']
    
    if password != password_check:
      raise ValidationError('비밀번호가 일치하지 않습니다!', code='invalid')
  
    return data
  
class EmailValidationSerializer(serializers.Serializer):
  
  email = serializers.EmailField(validators=[
    FormatValidator('유효한 이메일 형식이 아닙니다.', r'[a-z0-9_]+@[a-z]+\.[a-z]{2,3}'),
    UniqueValidator(queryset=User.objects.all(), message='이미 존재하는 이메일입니다.')
  ])