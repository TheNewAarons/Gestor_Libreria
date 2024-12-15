from django.db import models

# Create your models here.

class Editorial(models.Model):
    name = models.CharField(max_length=100, unique=True,)
    address = models.CharField(max_length=100, unique=True)
    phone = models.CharField(null=True, blank=True, unique=True, max_length=20)

    def __str__(self):
        return self.name