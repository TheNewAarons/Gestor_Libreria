from django.db import models
from Editoriales.models import Editorial
from Usuarios.models import Users

# Create your models here.
 
class Libro(models.Model):
    ESTADO_CHOICES = [
        ('Libro', 'Libro'),
        ('Revista', 'Revista'),
        ('Enciclopedias', 'Enciclopedias'),
    ]
    ESTADO_CHOICES2 = [
        ('Revision', 'Revisión'),
        ('Publicado', 'Publicado'),
        ('Denegado', 'Denegado')
    ]
    title = models.CharField(max_length=200, unique=True)
    tipo = models.CharField(max_length = 100, choices=ESTADO_CHOICES)
    tamaño = models.PositiveIntegerField(null=True, blank=True)
    cantidad = models.PositiveIntegerField(default=0)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)  # Relación con Editorial
    author = models.ForeignKey(Users, on_delete=models.CASCADE) # Relacion con author
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    portada = models.ImageField(upload_to="portada")
    estadoLibro = models.CharField(max_length=9, choices=ESTADO_CHOICES2, null=True)

    def __str__(self):
        return self.title
    
    def validar_stock(self, cantidad_solicitada):
        return self.cantidad >= cantidad_solicitada