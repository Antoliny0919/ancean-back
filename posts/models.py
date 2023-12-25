from django.db import models
from users.models import User
from category.models import Category

# Create your models here.

class PostManager(models.Manager):  
  
  foreign_fields_table = {
    "author": User,
    "category": Category,
  }
  
  def string_to_foreign_obj(self, **foreign_fields):

    field = {key: (self.__class__.foreign_fields_table[key]).objects.get(name=value)
            for key, value in foreign_fields.items()}

    return field
  
  def save_post(self, title, **extra_fields):

    return {'hello': 'world'}
    
  
  
  def create_post(self, title, is_finish, **extra_fields):
    
    post_fields = {}
    
    foreign_fields = extra_fields.pop("foreignFields")
    
    foreign_objs = self.string_to_foreign_obj(**foreign_fields)
    post_fields.update(foreign_objs)
    
    if is_finish:
      category = post_fields["category"]
      category.post_count += 1
      
    post_fields.update(extra_fields)

    post = self.model(
      title=title,
      is_finish=is_finish,
      **post_fields,
    )
    
    post.save()
    
    return {"id": post.id}


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
    
    
    
