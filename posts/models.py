from django.db import models
from users.models import User
from category.models import Category

# Create your models here.

class PostManager(models.Manager):  
  
  def save_post(self, title, **extra_fields):

    return {'hello': 'world'}
    
  
  
  def create_post(self, **fields):
    
    is_finish = fields["is_finish"]
    
    if is_finish:
      category = fields["category"]
      category.post_count += 1
      category.save()

    post = self.model(
      **fields
    )
    
    post.save()
    
    return post


class Post(models.Model):
  
  objects = PostManager()
  
  header_image = models.ImageField(null=True)
  title = models.CharField(max_length=100)
  content = models.JSONField('json', default=dict, null=True, blank=True)
  author = models.ForeignKey(User, on_delete=models.CASCADE, db_column="author", related_name='author')
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, db_column="category", related_name='category', null=True, blank=True)
  wave = models.IntegerField(default=0) # wave field like 'like post' on general SNS
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  is_finish = models.BooleanField(default=False)
  is_public = models.BooleanField(default=False)
  
  def __str__(self):
    return f'{self.title} - {self.author}'
    
    
    
