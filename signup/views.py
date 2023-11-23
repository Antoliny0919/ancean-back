import random
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import EmailValidationSerializer, UserValidationSerializer
from users.models import User
from authentication.views import get_token_for_user, success_response_with_jwt

# Create your views here.

class CreateUserView(APIView):
  
  def post(self, request):
    '''
    recieve front signup form data for createuser
    email and introduce fields do not validate --> check UserSerialzier
    email has a separate validation logic(EmailFieldSerializer) and has already been validated at the time the function is called
    introduce is none require field
    '''
    body = request.data
    serializer = UserValidationSerializer(data=body)
    if serializer.is_valid():
      # password1, password2 --> password
      user_data = {**serializer.data, 'password': serializer.data['password1']}
      del user_data['password1'], user_data['password2']
      User.objects.create_user(
        **user_data
      )
      # response with jwt token(access, refresh) when user creation is successful
      created_user = get_object_or_404(User, email=user_data['email'])
      token = get_token_for_user(created_user)
      response = success_response_with_jwt(created_user, token, status.HTTP_201_CREATED)
      
      return response
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SendAuthcodeEmailView(APIView):
  '''
  email validation(unique, type) before sending authentication code to email
  '''
  
  def post(self, request):
    body = request.data
    serializer = EmailValidationSerializer(data=body)
    if serializer.is_valid():
      email = body.get('email')
      title = 'ANcean 인증 코드'
      authentication_code = random.randint(100000, 1000000)
      body = f'''
      다음 코드를 입력하여 이메일 인증을 완료하세요.
      {authentication_code}
      '''
      email = EmailMessage(subject=title, body=body, to=[f'{email}'])
      try:
        email.send()
        return Response({'authcode': authentication_code, 'message': '인증번호를 입력해 주세요.'}, status=status.HTTP_200_OK)
      except: 
        Response({'hello': '전송실패'}, status=status.HTTP_400_BAD_REQUEST)
    else:
      print(serializer.errors)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)