from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    cellphone_number = models.CharField(max_length=20, blank=True, null=True) # Lo hago opcional
    country = models.CharField(max_length=100, blank=True)
    planet = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    genre = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.username
