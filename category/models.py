from django.db import models

# Create your models here.

class Category(models.Model):
  
  name = models.CharField(max_length=30, unique=True)
  post_count = models.IntegerField(default=0)
  
  def __str__(self):
    return f'{self.name}' 