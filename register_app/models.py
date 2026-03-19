from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):

    class Role(models.TextChoices):
        RIDER  = 'rider',  'Rider'
        DRIVER = 'driver', 'Driver'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.RIDER,
    )