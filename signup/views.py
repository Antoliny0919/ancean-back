import random
from django.core.mail import EmailMessage
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import EmailFieldSerializer

# Create your views here.

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
        return Response({'hello': '전송완료'}, status=status.HTTP_200_OK)
      except: 
        Response({'hello': '전송실패'}, status=status.HTTP_400_BAD_REQUEST)
    else:
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)