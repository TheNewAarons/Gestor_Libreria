from django.contrib import admin
from django.urls import path, include
from Libros.views import LibroListView
from Libreria import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('Libros/', include('Libros.urls')),
]
