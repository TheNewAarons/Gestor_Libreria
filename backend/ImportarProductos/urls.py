from django.urls import path
from ImportarProductos import views

urlpatterns = [
    path('importar/', views.importar_productos, name='importar_productos'),
]
