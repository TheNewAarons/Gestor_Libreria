from django.urls import path
from . import views

urlpatterns = [
    path('importar/', views.importar_productos, name='importar_productos'),
]
