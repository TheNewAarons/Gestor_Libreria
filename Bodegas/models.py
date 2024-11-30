from django.db import models
from Libros.models import Libro

# Create your models here.

class Bodega(models.Model):
    ESTADO_CHOICES = [
        ('VA', 'Vacio'),
        ('OC', 'Ocupado'),
        ('MT', 'Mantenimiento'),
    ]
    nombre = models.TextField(max_length=200, unique=True)
    direction = models.TextField(max_length=100, unique=True)
    tipo_de_contenido = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField(null=True, blank=True)
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES, default='BA')
    nivel_stock = models.IntegerField(default=0)
    tamaño_bodega = models.PositiveIntegerField(null=True, blank=True)
    bodega_origen = models.CharField(max_length=100, null=True, blank=True)
    bodega_destino = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.nombre


class ProductoBodega(models.Model):
    producto = models.ForeignKey(Libro, on_delete=models.CASCADE)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def _str_(self):
        return self.bodega