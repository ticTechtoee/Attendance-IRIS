from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
USER_ROLES = (
        ('Student', 'Student'),
    )

class User(AbstractUser):
    user_role = models.CharField(
        max_length=15, choices=USER_ROLES, default="Student")