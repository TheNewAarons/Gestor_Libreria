from django.db import models

# Create your models here.
class Editorial(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.IntegerField()

    def __str__(self):
        return self.name
    
class Users(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    rol = models.CharField(max_length=100)

class Author(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.name} {self.last_name}"

class Libro(models.Model):
    ESTADO_CHOICES = [
        ('Libro', 'Libro'),
        ('Revista', 'Revista'),
        ('Diccionario', 'Diccionario'),
    ]
    title = models.CharField(max_length=200)
    tipo = models.CharField(max_length = 100, null=True, choices=ESTADO_CHOICES)
    tamaño = models.PositiveIntegerField(null=True)
    editorial = models.CharField(max_length=100, null=True)
    author = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    portada = models.ImageField(null=True, blank=True, upload_to="portada")

    def __str__(self):
        return self.title