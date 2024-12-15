from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import UserPassesTestMixin
from Libros.forms import LibroForm
from Libros.models import Libro
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Sum
from Bodegas.models import ProductoBodega

# Create your views here.
class RolRequeridoMixin(UserPassesTestMixin):
    rol_requerido = 'Jefe de Bodega' 

    #Funcion para obtener el rol del usuario y restringir la vista, igual en las demas ya que va basado en nuestros requerimientos
    def test_func(self): #Va a evaluar que el usuario corresponda al rol que usemos para las restricciones
        return self.request.user.rol == self.rol_requerido

    #Funcion para redirigir al usuario que ingrese a la vista sin estar registrado o si inicio sesion con otro rol, hacia una pagina con un mensaje
    def handle_no_permission(self):
        return redirect('no_autorizado') 

#Funcion para mostrar en una pagina un mensaje sobre el acesso al sistema mediante un error 403
def no_autorizado(request):
    return render(request, 'Usuarios/ventanaError.html', status=403)

class LibroListView(RolRequeridoMixin,ListView):
    model = Libro
    template_name = 'libros/libros_list.html'
    context_object_name = 'libros'
    rol_requerido = 'Jefe de Bodega'

class LibroCreateView(RolRequeridoMixin,CreateView):
    model = Libro
    template_name = 'libros/libros_create.html'
    form_class = LibroForm
    success_url = reverse_lazy('list')
    rol_requerido = 'Jefe de Bodega'

class LibroDeleteView(RolRequeridoMixin,DeleteView):
    model = Libro
    template_name = 'libros/libros_delete.html'
    success_url = reverse_lazy('list')
    context_object_name = 'libros'
    rol_requerido = 'Jefe de Bodega'

class LibroUpdateView(RolRequeridoMixin,UpdateView):
    model = Libro
    template_name = 'libros/libros_update.html'
    form_class = LibroForm
    success_url = reverse_lazy('list')
    rol_requerido = 'Jefe de Bodega'

class LibroDetailView(RolRequeridoMixin,DetailView):
    model = Libro
    template_name = 'libros/libros_detail.html'
    context_object_name = 'libro'
    rol_requerido = 'Jefe de Bodega'

class LibroDeleteListView(RolRequeridoMixin, ListView):
    model = Libro
    template_name = 'libros/libros_delete_list.html'
    context_object_name = 'libros'
    rol_requerido = 'Jefe de Bodega'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener el stock de cada libro
        for libro in context['libros']:
            stock_total = ProductoBodega.objects.filter(
                producto=libro
            ).aggregate(
                total=Sum('cantidad')
            )['total'] or 0
            libro.stock_total = stock_total
        return context
    
    
class LibroDetailListView(RolRequeridoMixin, ListView):
    model = Libro
    template_name = 'libros/libros_detail_list.html'
    context_object_name = 'libros'
    rol_requerido = 'Jefe de Bodega'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener el stock de cada libro
        for libro in context['libros']:
            stock_total = ProductoBodega.objects.filter(
                producto=libro
            ).aggregate(
                total=Sum('cantidad')
            )['total'] or 0
            libro.stock_total = stock_total
        return context
    
class LibroEditListView(RolRequeridoMixin, ListView):
    model = Libro
    template_name = 'libros/libros_edit_list.html'
    context_object_name = 'libros'
    rol_requerido = 'Jefe de Bodega'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener el stock de cada libro
        for libro in context['libros']:
            stock_total = ProductoBodega.objects.filter(
                producto=libro
            ).aggregate(
                total=Sum('cantidad')
            )['total'] or 0
            libro.stock_total = stock_total
        return context