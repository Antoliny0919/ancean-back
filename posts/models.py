from django.db import models
from users.models import User
from category.models import Category

# Create your models here.

class Post(models.Model):
  header_image = models.ImageField(null=True)
  title = models.CharField(max_length=100)
  content = models.JSONField('json', default=dict, null=True, blank=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE, db_column="author", related_name='post')
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, db_column="category", related_name='post', null=True)
  wave = models.IntegerField(default=0) # wave field like 'like post' on general SNS
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  is_finish = models.BooleanField(default=False)
  is_public = models.BooleanField(default=False)
  
  def __str__(self):
    return f'{self.title} - {self.author}'