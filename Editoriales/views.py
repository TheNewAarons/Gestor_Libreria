from django.shortcuts import redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from Editoriales.forms import EditorialForm
from django.urls import reverse_lazy
from Editoriales.models import Editorial
from django.contrib import messages
from Libros.models import Libro
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
class EditorialListView(RolRequeridoMixin,ListView):
    model = Editorial
    template_name = 'Editoriales/editorialList.html'
    context_object_name = 'editoriales'
    rol_requerido = 'Jefe de Bodega'

class EditorialCreateView(RolRequeridoMixin,CreateView):
    model = Editorial
    form_class = EditorialForm
    template_name = 'Editoriales/editorialCreate.html'
    success_url  = reverse_lazy('editorialList')
    rol_requerido = 'Jefe de Bodega'

class EditorialDeleteView(RolRequeridoMixin,DeleteView):
    model = Editorial
    template_name = 'Editoriales/editorialDelete.html'
    success_url = reverse_lazy('editorialList')
    rol_requerido = 'Jefe de Bodega'

class EditorialUpdateView(RolRequeridoMixin,UpdateView):
    model = Editorial
    form_class = EditorialForm
    template_name = 'Editoriales/editorialUpdate.html'
    success_url = reverse_lazy('editorialList')
    rol_requerido = 'Jefe de Bodega'

class EditorialEditListView(RolRequeridoMixin, ListView):
    model = Editorial
    template_name = 'Editoriales/editorial_edit_list.html'
    context_object_name = 'editoriales'
    rol_requerido = 'Jefe de Bodega'

class EditorialDeleteListView(RolRequeridoMixin, ListView):
    model = Editorial
    template_name = 'Editoriales/editorial_delete_list.html'
    context_object_name = 'editoriales'
    rol_requerido = 'Jefe de Bodega'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadir el conteo de productos a cada editorial
        for editorial in context['editoriales']:
            editorial.productos_count = Libro.objects.filter(editorial=editorial).count()
        return context

class EditorialDeleteView(RolRequeridoMixin, DeleteView):
    model = Editorial
    template_name = 'Editoriales/editorial_confirm_delete.html'  # Actualizado
    success_url = reverse_lazy('editorial_delete_list')
    rol_requerido = 'Jefe de Bodega'

    def post(self, request, *args, **kwargs):
        editorial = self.get_object()
        if Libro.objects.filter(editorial=editorial).exists():
            messages.error(request, 'No se puede eliminar la editorial porque tiene productos asociados.')
            return redirect('editorial_delete_list')
        messages.success(request, 'Editorial eliminada exitosamente.')
        return super().post(request, *args, **kwargs)