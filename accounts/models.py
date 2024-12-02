from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.managers import CustomUserManager


class User(AbstractUser):
    """
    Модель сущности пользователя.
    """
    username = None
    email = models.EmailField(_("email address"), unique=True)
    is_active = models.BooleanField(default=True)
    role = models.CharField(max_length=45, default="user")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
