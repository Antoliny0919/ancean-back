from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin


class CustomUserManager(UserManager):

  def _create_user(self, email, password, **extra_fields):
      """
      Create and save a user with the given username, email, and password.
      """
      if not email:
          raise ValueError("The given username must be set")
      email = self.normalize_email(email)
      # Lookup the real model class from the global app registry so this
      # manager method can be used in migrations. This is fine because
      # managers are by definition working on the real model.
      user = self.model(email=email, **extra_fields)
      user.password = make_password(password)
      user.save(using=self._db)
      return user

  def create_user(self, email, password, **extra_fields):
      extra_fields.setdefault("is_staff", False)
      extra_fields.setdefault("is_superuser", False)
      return self._create_user(email, password, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
      extra_fields.setdefault("is_staff", True)
      extra_fields.setdefault("is_superuser", True)

      if extra_fields.get("is_staff") is not True:
          raise ValueError("Superuser must have is_staff=True.")
      if extra_fields.get("is_superuser") is not True:
          raise ValueError("Superuser must have is_superuser=True.")

      return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
  
  objects = CustomUserManager()
  
  email = models.EmailField(max_length=255, unique=True)
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
  
  class Meta:
    app_label = 'users'
    
  def __str__(self):
    return self.email