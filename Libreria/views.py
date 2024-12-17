from django.shortcuts import render
from Usuarios.models import Users
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
def home(request):
    return render(request, 'Libreria/Home.html')

class BaseView(LoginRequiredMixin, TemplateView):
    template_name = 'Libreria/Base_Modulos.html'
    
def contacto(request):
    return render(request, 'Libreria/Seccion_Contacto.html')

class SeccionInformesView(LoginRequiredMixin, TemplateView):
    template_name = 'Libreria/Seccion_informes.html'