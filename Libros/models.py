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
    title = models.CharField(max_length=200, unique=True)
    tipo = models.CharField(max_length = 100, choices=ESTADO_CHOICES)
    tamaño = models.PositiveIntegerField()
    cantidad = models.PositiveIntegerField(default=0)
    editorial = models.ForeignKey(Editorial, on_delete=models.CASCADE)  # Relación con Editorial
    author = models.ForeignKey(Users, on_delete=models.CASCADE) # Relacion con author
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    portada = models.ImageField(upload_to="portada")

    def __str__(self):
        return self.title
    
    def validar_stock(self, cantidad_solicitada):
        return self.cantidad >= cantidad_solicitada