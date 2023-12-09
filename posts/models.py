from django.db import models
from users.models import User
from category.models import Category

# Create your models here.

class Post(models.Model):
  header_image = models.ImageField()
  title = models.CharField(max_length=100)
  content = models.TextField()
  author = models.ForeignKey(User, on_delete=models.CASCADE, db_column="author", related_name='post')
  category = models.ForeignKey(Category, on_delete=models.SET_NULL, db_column="category", related_name='post', null=True)
  # wave field like 'like post' on general SNS
  wave = models.IntegerField(default=0)
  
  def __str__(self):
    return f'{self.title} - {self.author}'