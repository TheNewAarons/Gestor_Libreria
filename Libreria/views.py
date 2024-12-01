from django.shortcuts import render
from Usuarios.models import Users
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
def home(request):
    return render(request, 'Libreria/Home.html')

class BaseView(LoginRequiredMixin, TemplateView):
    template_name = 'Libreria/Base_Modulos.html'
    
def page_not_found_view(request, exception):
    return render(request, 'Libreria/errorPag.html', status=404) 

def contacto(request):
    
    return render(request, 'Libreria/Seccion_Contacto.html')