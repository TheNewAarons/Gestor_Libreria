from django.urls import path, include
from GestorLibreria import settings
from Libros import views
from Libros.views import LibroCreateView, LibroListView, LibroDeleteView, LibroUpdateView, LibroDetailView

urlpatterns = [
    path('base/', views.base, name='base'),
    path('list/', LibroListView.as_view(), name='list'),
    path('create/', LibroCreateView.as_view(), name='create'),
    path('delete/<int:pk>/', LibroDeleteView.as_view(), name='delete'),
    path('update/<int:pk>/', LibroUpdateView.as_view(), name='update'),
    path('detail/<int:pk>/', LibroDetailView.as_view(), name='detail'),
]
