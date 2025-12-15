from rest_framework import viewsets, decorators, status
from rest_framework.response import Response
from .models import Libro
from .serializers import LibroSerializer
from Usuarios.permissions import IsJefeDeBodega

class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
    # Usamos IsAuthenticated por defecto desde settings, pero si quieres restringir todo a Jefe:
    # permission_classes = [IsJefeDeBodega] 
    # Dejamos abierto a Autores según lógica de negocio original (crear libros)

    def perform_create(self, serializer):
        # Asignar autor y estado automáticamente
        user = self.request.user
        estado_libro = 'Revision' if user.rol == 'Autor' else 'Publicado'
        serializer.save(author=user, estadoLibro=estado_libro)

    @decorators.action(detail=True, methods=['post'])
    def cambiar_estado(self, request, pk=None):
        libro = self.get_object()
        nuevo_estado = request.data.get('estadoLibro')
        
        if nuevo_estado not in ['Publicado', 'Denegado']:
             return Response({'error': 'Estado no válido'}, status=status.HTTP_400_BAD_REQUEST)

        libro.estadoLibro = nuevo_estado
        libro.save()
        return Response({'message': f'Estado actualizado a {nuevo_estado}'})