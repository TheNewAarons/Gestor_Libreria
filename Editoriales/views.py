from django.http import JsonResponse
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

def format_phone_number(phone):
    #va a formatear el numero de este modo 9 1234 1234
    phone = str(phone)
    if len(phone) == 9:
        return f"{phone[0]} {phone[1:5]} {phone[5:]}"
    return phone  #si no tiene 9 caracteres,devolver el número tal cual
class EditorialListView(RolRequeridoMixin,ListView):
    model = Editorial
    template_name = 'Editoriales/editorialList.html'
    context_object_name = 'editoriales'
    rol_requerido = 'Jefe de Bodega'
    def get_context_data(self, **kwargs):
        #Se obtiene el contexto por defecto
        context = super().get_context_data(**kwargs)
        
        #formateamos los datos del telefono
        for editorial in context['editoriales']:
            editorial.phone = format_phone_number(editorial.phone)
        
        return context

class EditorialCreateView(RolRequeridoMixin,CreateView):
    model = Editorial
    form_class = EditorialForm
    template_name = 'Editoriales/editorialCreate.html'
    success_url  = reverse_lazy('editorialList')
    rol_requerido = 'Jefe de Bodega'
    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({
            "success": True,
            "message": "Editorial creada con éxito."
        })

    def form_invalid(self, form):
        return JsonResponse({
            "success": False,
            "errors": form.errors
        }, status=400)
    
class EditorialDeleteView(RolRequeridoMixin,DeleteView):
    model = Editorial
    template_name = 'Editoriales/editorialDelete.html'
    success_url = reverse_lazy('editorialList')
    rol_requerido = 'Jefe de Bodega'
    def get_object(self, queryset=None):
        editorial = Editorial.objects.get(id=self.kwargs['editorial_id'])
        
        # Verifica si la editorial tiene productos asociados
        if editorial.productos.count() > 0:
            return redirect('editorial_list')  # Redirige si tiene productos asociados

        return editorial

class EditorialUpdateView(RolRequeridoMixin,UpdateView):
    model = Editorial
    form_class = EditorialForm
    template_name = 'Editoriales/editorialUpdate.html'
    success_url = reverse_lazy('editorialList')
    rol_requerido = 'Jefe de Bodega'
    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({
            "success": True,
            "message": "Editorial creada con éxito."
        })

    def form_invalid(self, form):
        return JsonResponse({
            "success": False,
            "errors": form.errors
        }, status=400)
    
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        editorial = self.get_object()  #obtenemos el objeto del usuario con la id (pk) de la URL
        context['username'] = editorial.name  #agrega el username al contexto para usarlo en la plantilla
        return context


    def post(self, request, *args, **kwargs):
        editorial = self.get_object()
        #se va a eliminar el usuario
        try:
            editorial.delete()
            #si resulta exitosos devuelve una respuesta en json
            return JsonResponse({
                'success': True,
                'message': 'Usuario eliminado con éxito.'
            })
        except Exception as e:
            #si resulta que hay error devuelve el mensaje de error 
            return JsonResponse({
                'success': False,
                'message': f'Error al eliminar el usuario: {str(e)}'
            }, status=400)