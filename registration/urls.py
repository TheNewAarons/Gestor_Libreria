from django.urls import path
from registration.views import CustomLoginView
urlpatterns = [
    path('login', CustomLoginView.as_view(), name='InicioSesion')
]
