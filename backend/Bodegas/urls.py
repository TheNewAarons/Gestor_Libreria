from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .views import BodegaViewSet, MovimientoProductoViewSet, ProductoBodegaViewSet

router = SimpleRouter()
router.register(r'bodegas', BodegaViewSet)
router.register(r'movimientos', MovimientoProductoViewSet)
router.register(r'productos-bodega', ProductoBodegaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
