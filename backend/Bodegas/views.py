from rest_framework import viewsets, status, decorators
from rest_framework.response import Response
from django.db import transaction, models
from django.db.models import Sum
from rest_framework.exceptions import ValidationError
from .models import Bodega, MovimientoProducto, ProductoBodega
from .serializers import BodegaSerializer, MovimientoProductoSerializer, ProductoBodegaSerializer
from Libros.models import Libro
from Usuarios.models import Users
from Usuarios.permissions import IsJefeDeBodega

class BodegaViewSet(viewsets.ModelViewSet):
    queryset = Bodega.objects.all()
    serializer_class = BodegaSerializer
    permission_classes = [IsJefeDeBodega]

    def perform_destroy(self, instance):
        if instance.nivel_stock > 0 or instance.estado != 'VA':
            raise ValidationError("No se puede eliminar una bodega que no esté vacía.")
        instance.delete()

    @decorators.action(detail=True, methods=['get'])
    def productos(self, request, pk=None):
        bodega = self.get_object()
        productos = ProductoBodega.objects.filter(bodega=bodega, cantidad__gt=0)
        serializer = ProductoBodegaSerializer(productos, many=True)
        return Response(serializer.data)

    @decorators.action(detail=False, methods=['post'])
    def mover_producto(self, request):
        bodega_origen_id = request.data.get('bodega_origen')
        bodega_destino_id = request.data.get('bodega_destino')
        producto_id = request.data.get('producto')
        cantidad = int(request.data.get('cantidad', 0))

        if not all([bodega_origen_id, bodega_destino_id, producto_id, cantidad]):
             return Response({'error': 'Faltan datos requeridos'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                bodega_origen = Bodega.objects.select_for_update().get(pk=bodega_origen_id)
                bodega_destino = Bodega.objects.select_for_update().get(pk=bodega_destino_id)
                producto = Libro.objects.get(pk=producto_id)

                # Verificar stock
                producto_bodega_origen = ProductoBodega.objects.filter(
                    bodega=bodega_origen, producto=producto
                ).first()

                if not producto_bodega_origen or producto_bodega_origen.cantidad < cantidad:
                     return Response({'error': 'Stock insuficiente en bodega de origen'}, status=status.HTTP_400_BAD_REQUEST)

                # Actualizar origen
                producto_bodega_origen.cantidad -= cantidad
                producto_bodega_origen.save()

                # Actualizar destino
                producto_bodega_destino, _ = ProductoBodega.objects.get_or_create(
                    bodega=bodega_destino, producto=producto,
                    defaults={'cantidad': 0}
                )
                producto_bodega_destino.cantidad += cantidad
                producto_bodega_destino.save()

                # Crear registro de movimiento
                MovimientoProducto.objects.create(
                    bodega_origen=bodega_origen,
                    bodega_destino=bodega_destino,
                    producto=producto,
                    cantidad=cantidad,
                    usuario=request.user if request.user.is_authenticated else None
                )

                # Actualizar totales y estados
                bodega_origen.nivel_stock = ProductoBodega.objects.filter(bodega=bodega_origen).aggregate(Sum('cantidad'))['cantidad__sum'] or 0
                bodega_destino.nivel_stock = ProductoBodega.objects.filter(bodega=bodega_destino).aggregate(Sum('cantidad'))['cantidad__sum'] or 0

                bodega_origen.actualizar_estado()
                bodega_destino.actualizar_estado()

            return Response({'message': 'Movimiento realizado exitosamente'})

        except Bodega.DoesNotExist:
            return Response({'error': 'Bodega no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Libro.DoesNotExist:
            return Response({'error': 'Libro no encontrado'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class MovimientoProductoViewSet(viewsets.ModelViewSet):
    queryset = MovimientoProducto.objects.all()
    serializer_class = MovimientoProductoSerializer

class ProductoBodegaViewSet(viewsets.ModelViewSet):
    queryset = ProductoBodega.objects.all()
    serializer_class = ProductoBodegaSerializer