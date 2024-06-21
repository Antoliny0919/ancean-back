from django.db import models
from posts.models import Post
from users.models import User

# Create your models here.

class Project(models.Model):
  
  # header_image --> symbol of the project image
  header_image = models.ImageField()
  title = models.CharField(max_length=36)
  description = models.TextField(default='')
  posts = models.ForeignKey(Post, on_delete=models.PROTECT, related_name='project')
  creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project')
  created_at = models.DateField(auto_now_add=True)
  updated_at = models.DateTimeField(null=True)
  
  def __str__(self):
    return self.title
  