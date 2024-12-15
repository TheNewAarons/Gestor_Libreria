from django.db import models
from Libros.models import Libro
from django.core.exceptions import ValidationError

# Create your models here.

class Bodega(models.Model):
    ESTADO_CHOICES = [
        ('VA', 'Vacio'),
        ('OC', 'Ocupado'),
        ('MT', 'Mantenimiento'),
    ]
    nombre = models.CharField(max_length=200, unique=True)
    direction = models.CharField(max_length=100, unique=True)
    tipo_de_contenido = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField(null=True, blank=True)
    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES, default='BA')
    nivel_stock = models.IntegerField(default=0)
    tamaño_bodega = models.PositiveIntegerField(null=True, blank=True)
    bodega_origen = models.CharField(max_length=100, null=True, blank=True)
    bodega_destino = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    productos = models.ManyToManyField(Libro, through='ProductoBodega')

    def clean(self):
        # Solo validar unicidad si es una nueva instancia (no una actualización)
        if not self.pk:  # si no tiene pk, es una nueva instancia
            if Bodega.objects.filter(nombre=self.nombre).exists():
                raise ValidationError('Ya existe una bodega con este nombre')
            if Bodega.objects.filter(direction=self.direction).exists():
                raise ValidationError('Ya existe una bodega con esta dirección')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def agregar_producto(self, producto, cantidad):
        producto_bodega, created = ProductoBodega.objects.get_or_create(
            producto=producto,
            bodega=self,
            defaults={'cantidad': cantidad}
        )
        if not created:
            producto_bodega.cantidad += cantidad
            producto_bodega.save()
        
        self.nivel_stock += cantidad
        self.save()

    def obtener_productos(self):
        """Retorna todos los productos en la bodega"""
        return ProductoBodega.objects.filter(bodega=self)

    def actualizar_estado(self):
        """Actualiza el estado de la bodega basado en su nivel de stock"""
        if self.nivel_stock == 0:
            self.estado = 'VA'
        else:
            self.estado = 'OC'
        self.save()

    def __str__(self):
        return self.nombre


class ProductoBodega(models.Model):
    producto = models.ForeignKey(Libro, on_delete=models.CASCADE)
    bodega = models.ForeignKey(Bodega, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"{self.bodega.nombre}"