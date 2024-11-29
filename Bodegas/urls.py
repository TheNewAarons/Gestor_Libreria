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
    path('retirar_producto/', views.retirar_producto_bodega, name='retirar_producto_bodega'),
]
