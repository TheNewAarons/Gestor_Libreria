from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Users(AbstractUser):
    ROL_CHOISE = [
        ('Autor', 'Autor'),
        ('Bodeguero', 'Bodeguero'),
        ('Jefe de Bodega', 'Jefe de bodega')
        
    ]
    username = models.CharField(max_length=100, unique=True)
    rol = models.CharField(max_length=50, choices=ROL_CHOISE, default='Bodeguero')
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='usuarios_groups',  # Cambia el nombre de la relación inversa
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='usuarios_user_permissions',  # Cambia el nombre de la relación inversa
        blank=True
    )
    def __str__(self):
        return self.username 