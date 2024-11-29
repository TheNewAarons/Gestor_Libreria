from django.urls import path
from Usuarios.views import UsuarioListView, UsuarioCreateView, UsuarioDeleteView, UsuarioUpdateView, UsuarioDetailView
from . import views

urlpatterns = [
    path('listUsuarios/', UsuarioListView.as_view(), name = 'userList'),
    path('CreateUsuarios/', UsuarioCreateView.as_view(), name = 'userCreate'),
    path('DeleteUsuarios/<int:pk>', UsuarioDeleteView.as_view(), name = 'userDelete'),
    path('UpdateUsuarios/<int:pk>', UsuarioUpdateView.as_view(), name = 'userUpdate'),
    path('DetailUsuarios/<int:pk>', UsuarioDetailView.as_view(), name = 'userDetail'),
    path('no-autorizado/', views.no_autorizado, name='no_autorizado') #view para el aviso sobre el ingreso no autorizado al sistema
    
]