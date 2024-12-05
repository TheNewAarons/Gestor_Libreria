from django.urls import path, include
from . import views
from GestorLibreria import settings
from Bodegas.views import BodegasListView, BodegasCreateView, BodegasDeleteView, BodegasDetailView, BodegasUpdateView

urlpatterns = [
    path('bodegas_list/', BodegasListView.as_view(), name='bodegas_list'),
    path('bodegas_create/', BodegasCreateView.as_view(), name='bodegas_create'),
    path('bodegas_delete/<int:pk>/', BodegasDeleteView.as_view(), name='bodegas_delete'),
    path('bodegas_detail/<int:pk>/', BodegasDetailView.as_view(), name='bodegas_detail'),
    path('bodegas_update/<int:pk>/', BodegasUpdateView.as_view(), name='bodegas_update'),
    path('agregar_producto/', views.agregar_producto_bodega, name='agregar_producto_bodega'),
    path('retirar-producto/', views.retirar_producto_bodega, name='retirar_producto_bodega'),
    path('retirar-producto/<int:bodega_id>/', views.retirar_producto_bodega, name='retirar_producto_bodega_detail'),
    path('mover-producto/', views.mover_producto, name='mover_producto'),
    path('get-productos-bodega/', views.get_productos_bodega, name='get_productos_bodega'),
    path('eliminar-bodegas/', views.eliminar_bodegas_view, name='eliminar_bodegas'),
    path('bodegas_detail_list/', views.bodegas_detail_list, name='bodegas_detail_list'),
    path('editar-bodegas/', views.editar_bodegas_list, name='editar_bodegas_list'),
    path('editar-bodega/<int:pk>/', views.editar_bodega, name='editar_bodega'),
]
