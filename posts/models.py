from django.db import models
from django.utils import timezone
from django_prometheus.models import ExportModelOperationsMixin
from users.models import User
from category.models import Category

# Create your models here.

class PostManager(models.Manager):
  
  def set_related_category(self, category, is_finish, instance_is_finish):
    
    if (is_finish and instance_is_finish == None):
      category.post_count += 1
      category.save()
      return
    
    if (is_finish != bool(instance_is_finish)):
      if is_finish:
        category.post_count += 1
        category.save()
      else:
        category.post_count -= 1
        category.save()
      return

  def create_post(self, **fields):
    
    if (hasattr(fields, 'category') and fields['is_finish']):
      category, is_finish = fields['category'], fields['is_finish']
      fields['created_at'] = timezone.localtime()
      self.set_related_category(category, is_finish, None)

    post = self.model(
      **fields,
    )
    
    post.save()
    
    return post
  
  def save_post(self, instance, **fields):
    
    is_finish, instance_is_finish = fields['is_finish'], getattr(instance, 'is_finish')
    
    # if (hasattr(fields, 'category') and is_finish):
      # frist
      # if (instance_is_finish != is_finish):
        
      # if (not hasattr(instance, 'category')):
      #   category = fields['category']
      #   self.set_related_category(category, is_finish, instance_is_finish)
      # else:
      #   before_category = instance['category']
      #   after_category = fields['category']
      #   before_category.post_count -= 1
      #   before_category.save()
      #   after_category.post_count += 1
      #   after_category.save()
         
    
    if (is_finish and not bool(instance_is_finish)):
      fields['created_at'] = timezone.localtime()
    
    for field_name in fields.keys():
      if getattr(instance, field_name) != fields[field_name]:
        setattr(instance, field_name, fields[field_name])
        
      
    
    instance.save()
    return instance

    

  # def save_publish_post(self, instance, is_finish):
    
  #   category = getattr(instance, 'category')
  #   if category:
  #     category.post_count += 1
  #     category.save()
    
  #   now = timezone.localtime()
  #   setattr(instance, 'created_at', now)
  #   instance.save()
    
  #   return instance

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
  
    
    
