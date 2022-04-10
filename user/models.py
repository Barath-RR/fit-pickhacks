from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin


# Base User Manager
class BaseUserManagerOverride(BaseUserManager):
    def create_user(self, email, user_type, password, **extra_fields):
        if not email or not password:
            raise ValueError("Email or Password is not set.")
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, user_type, **extra_fields):
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_staff", True)
        if extra_fields.get("is_superuser") is False:
            raise ValueError("Superuser needs to be True.")
        if not user_type:
            user_type = "SUPERUSER"
        return self.create_user(email=email, password=password, user_type=user_type, **extra_fields)


# Basic Info User
class BaseUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=False)
    user_type = models.CharField(choices=(
        ('USER', 'USER'),
        ('SUPERUSER', 'SUPER_USER'),
    ), max_length=40)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']
    objects = BaseUserManagerOverride()

    class Meta:
        verbose_name = "All Users"
        verbose_name_plural = "All Users"

    def __str__(self):
        return self.email
    
class Profile(models.Model):
    id = models.AutoField(primary_key=True)
    username=models.CharField(blank=False, max_length=50)
    email = models.EmailField(blank=False)
    place = models.EmailField(blank=False)
    bio = models.CharField(max_length=250, blank=False)
    
