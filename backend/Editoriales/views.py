from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from .models import Editorial
from .serializers import EditorialSerializer
from Usuarios.permissions import IsJefeDeBodega

class EditorialViewSet(viewsets.ModelViewSet):
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializer
    permission_classes = [IsJefeDeBodega]

    def perform_destroy(self, instance):
        if instance.libro_set.exists():  # Asumiendo relación inversa por defecto 'libro_set'
            raise ValidationError("No se puede eliminar la editorial porque tiene libros asociados.")
        instance.delete()