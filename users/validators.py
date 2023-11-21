import re
from django.core.exceptions import ValidationError


length_error_message = '아이디는 4자 이상 16자 이하만 가능합니다.'

username_default_errors = {'max_length': length_error_message,
                      'min_length': length_error_message,
                      'blank': length_error_message}

address_default_errors = {
  'blank': '주소 검색을 진행해 주세요!'
}

class FormatValidator:
  
  def __init__(self, message, regex, code='invalid'):
    self.message = message
    self.regex = regex
    self.code = code
    
  def __call__(self, value):
    if not re.fullmatch(self.regex, value):
      raise ValidationError(self.message, code=self.code)