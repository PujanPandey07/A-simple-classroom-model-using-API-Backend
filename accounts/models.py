from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    RolE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    )
    role = models.CharField(
        max_length=20, choices=RolE_CHOICES, default='student')
