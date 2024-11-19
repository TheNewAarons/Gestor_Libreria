from django.db import models

# Create your models here.

class Users(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    rol = models.CharField(max_length=100)

    def __str__(self):
        return self.username 