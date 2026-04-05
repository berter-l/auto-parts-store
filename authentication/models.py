from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from authentication.managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    Groups = [
        ('S', 'Supplier'),
        ('U', 'User'),
        ('Super', 'Superuser'),
    ]
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    group = models.CharField(choices=Groups, max_length=5, default='U')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['username', 'password', 'email']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.email}'
