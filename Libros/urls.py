from django.urls import path, include
from Libros.views import LibroCreateView, LibroListView, LibroDeleteView, LibroUpdateView

urlpatterns = [
    path('list/', LibroListView.as_view(), name='list'),
    path('create/', LibroCreateView.as_view(), name='create'),
    path('delete/<int:pk>/', LibroDeleteView.as_view(), name='delete'),
    path('update/<int:pk>/', LibroUpdateView.as_view(), name='update'),
]