from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model. Defined before first migration per Django best practice.
    Uses AbstractUser to preserve all standard fields and admin integration.
    """
    mfa_enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        return self.email or self.username
