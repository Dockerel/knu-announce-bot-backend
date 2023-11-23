from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    
    """User Model Definition"""

    email = models.EmailField()
