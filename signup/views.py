import random
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import EmailFieldSerializer, UserSerializer
from users.models import User

# Create your views here.

class CreateUserView(APIView):
  
  def post(self, request):
    '''
    recieve front signup form data for createuser
    email and introduce fields do not validate
    email has a separate validation logic and has already been validated at the time the function is called
    introduce is none require field
    '''
    body = request.data
    serializer = UserSerializer(data=body)
    if serializer.is_valid():
      User.objects.create_user(
        email=body.get('email'),
        password=serializer.data['password1'],
        introduce=body.get('introduce')
      )
      return Response({'message', '회원가입 성공'}, status=status.HTTP_201_CREATED)
    else:
      Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendAuthcodeEmailView(APIView):
  
  def post(self, request):
    body = request.data
    serializer = EmailFieldSerializer(data=body)
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