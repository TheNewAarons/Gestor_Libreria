from django.db import models

# Create your models here.

class Editorial(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name