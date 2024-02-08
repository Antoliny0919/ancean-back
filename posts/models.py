from django.db import models
from django.utils import timezone
from django_prometheus.models import ExportModelOperationsMixin
from users.models import User
from category.models import Category

# Create your models here.

class PostManager(models.Manager):  
  
  def publish_post(self, **fields):
    
    # Increase the value of the post_count in the category associated with
    # the post at the time of initial publication
    if hasattr(fields, 'category'):
      category = fields['category']
      category.post_count += 1
      category.save()
      
    now = timezone.localtime()
    post = self.model(
      created_at=now,
      **fields,
    )
  
    post.save()
    
    return post

  def save_publish_post(self, instance, is_finish):
    
    category = getattr(instance, 'category')
    if category:
      category.post_count += 1
      category.save()
    
    now = timezone.localtime()
    setattr(instance, 'created_at', now)
    instance.save()
    
    return instance

class Post(ExportModelOperationsMixin('post'), models.Model):
  
  objects = PostManager()
  
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
  
    
    
