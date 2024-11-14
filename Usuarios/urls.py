from django.urls import path
from Usuarios.views import UsuarioListView, UsuarioCreateView, UsuarioDeleteView, UsuarioUpdateView, UsuarioDetailView
urlpatterns = [
    path('listUsuarios/', UsuarioListView.as_view(), name = 'userList'),
    path('CreateUsuarios/', UsuarioCreateView.as_view(), name = 'userCreate'),
    path('DeleteUsuarios/<int:pk>', UsuarioDeleteView.as_view(), name = 'userDelete'),
    path('UpdateUsuarios/<int:pk>', UsuarioUpdateView.as_view(), name = 'userUpdate'),
    path('DetailUsuarios/<int:pk>', UsuarioDetailView.as_view(), name = 'userDetail')
]