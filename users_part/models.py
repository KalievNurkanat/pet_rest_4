from django.db import models
from users_part.managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# Create your models here.

class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField()
    password = models.CharField()
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password"]

    def __str__(self):
        return f"{self.username}"