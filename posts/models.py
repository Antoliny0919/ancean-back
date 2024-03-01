from django.db import models
from django.utils import timezone
from django_prometheus.models import ExportModelOperationsMixin
from users.models import User
from category.models import Category

# Create your models here.

class Post(ExportModelOperationsMixin('post'), models.Model):
  
  header_image = models.ImageField(default='ancean-no-header-image.png')
  title = models.CharField(max_length=100)
  introduce = models.TextField(default='')
  content = models.JSONField('json', default=[{}], null=True, blank=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE, db_column="author", related_name='author')
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, db_column="category", related_name='category', null=True, blank=True)
  wave = models.IntegerField(default=0) # wave field like 'like post' on general SNS
  created_at = models.DateTimeField(null=True)
  updated_at = models.DateTimeField(auto_now=True)
  is_finish = models.BooleanField(default=False)
  is_public = models.BooleanField(default=False)
  
  def __str__(self):
    return f'{self.title} - {self.author}'
  
  @classmethod
  def get_all_fields_name(cls):
    fields = cls._meta.get_fields()
    fields_name = [field.name for field in fields]
    return fields_name
  
  @staticmethod
  def changing_public(instance=None, **fields):
    '''
    Post model object incidental processing before becomming public state
    '''

    # increase category post_count associated with foreign key when category field exist in validated_data
    if 'category' in fields: 
      category = fields['category']
      category.post_count += 1
      category.save()
      
    # none exist instance(first generated post)
    # or post that has already been created but is not in the public state set created_at data
    if ((instance == None) or getattr(instance, 'created_at') == None):
      print(1)
      fields['created_at'] = timezone.localtime()
    
    return fields
    
  @staticmethod
  def changing_private(instance):
    '''
    Post model object incidental processing before becomming private state
    '''
    
    # when a post becomes private, the number of post categories is also decrease
    if hasattr(instance, 'category'):
      category = getattr(instance, 'category')
      category.post_count -= 1
      category.save()
  
    
    
