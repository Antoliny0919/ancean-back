import os
import shutil
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.management.commands import createsuperuser
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin


class CustomUserManager(UserManager):

  def _create_user(self, email, _name, password, **extra_fields):
      """
      Create and save a user with the given email, name, and password.
      """
      if not email:
          raise ValueError("The given username must be set")
      email = self.normalize_email(email)
      # Lookup the real model class from the global app registry so this
      # manager method can be used in migrations. This is fine because
      # managers are by definition working on the real model.
      user = self.model(email=email, name=_name, **extra_fields)
      user.password = make_password(password)
      user.save(using=self._db)
      return user

  def create_user(self, email, _name, password, **extra_fields):
      extra_fields.setdefault("is_staff", False)
      extra_fields.setdefault("is_superuser", False)
      return self._create_user(email, _name, password, **extra_fields)

  def create_superuser(self, email, _name, password, **extra_fields):
      extra_fields.setdefault("is_staff", True)
      extra_fields.setdefault("is_superuser", True)

      if extra_fields.get("is_staff") is not True:
          raise ValueError("Superuser must have is_staff=True.")
      if extra_fields.get("is_superuser") is not True:
          raise ValueError("Superuser must have is_superuser=True.")

      return self._create_user(email, _name, password, **extra_fields)
    
  def delete_user(self, user):
    '''
    delete user logic
    remove the parts related to the user to be removed as well(image_storage)
    '''
    personal_image_storage = os.path.join(getattr(settings, 'MEDIA_ROOT'), f'{user.name}')
    if os.path.exists(personal_image_storage):
      shutil.rmtree(personal_image_storage, ignore_errors=True)
    user.delete()


class User(AbstractBaseUser, PermissionsMixin):
  
  objects = CustomUserManager()
  email = models.EmailField(max_length=255, unique=True)
  _name = models.CharField(max_length=20, unique=True, db_column="name")
  introduce = models.CharField(max_length=255, null=True)
  is_staff = models.BooleanField(
    default=False,
    help_text=("Designates whether the user can log into this admin site."),
  )
  is_active = models.BooleanField(
    default=True,
    help_text=(
        "Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts."
    ),
  )
  
  USERNAME_FIELD = 'email'
  
  REQUIRED_FIELDS = ['_name']
  
  class Meta:
    app_label = 'users'
    
  def __str__(self):
    return self.name
  
  @property
  def name(self):
    return self._name
  
  @name.setter
  def name(self, value):
    '''
    when the user was first created or the name was modified
    personal image storage change name together or create
    '''
    
    have_personal_image_storage = os.path.join(getattr(settings, 'MEDIA_ROOT'), f'{self._name}')
    new_personal_image_storage = os.path.join(getattr(settings, 'MEDIA_ROOT'), f'{value}')
    
    if self._name:
      os.rename(have_personal_image_storage, new_personal_image_storage)
    elif (not os.path.exists(new_personal_image_storage)): 
      os.mkdir(new_personal_image_storage)
      
    self._name = value
  