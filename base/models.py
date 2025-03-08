from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLES = (
        ('admin', 'Admin'),
        ('user', 'User'),
        ('owner', 'Owner'),
    )
    role = models.CharField(max_length=10, choices=ROLES, default='user')