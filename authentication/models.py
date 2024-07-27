from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser
        with the given email and password.
        """
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser):#, PermissionsMixin):
    """
    Basic user class
    """
    password = models.CharField(max_length=255)
    last_login = models.DateTimeField(auto_now=True)
    email = models.EmailField(max_length=50, unique=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return self.email