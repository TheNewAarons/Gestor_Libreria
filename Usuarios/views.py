from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from Usuarios.models import Users
from Usuarios.forms import UsersForm
from django.urls import reverse_lazy
from django.http import HttpResponse, JsonResponse
# Create your views here.

#Clase para poder asegurar las vistas para los diferentes roles que tenemos, esta clase funciona en base al rol que otorgemos y asi evitar que usuarios sin permisos ingresen a otras funcionalidades
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

class UsuarioListView(LoginRequiredMixin,RolRequeridoMixin,ListView):
    model = Users
    template_name = 'Usuarios/userList.html'
    context_object_name = 'usuarios'
    rol_requerido = 'Jefe de Bodega'
    login_url = 'registration/login.html'
    redirect_field_name = 'Usuarios/userList.html'
    def get_queryset(self):
        #obtengo todos los usuarios
        return Users.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agrega el usuario autenticado al contexto
        context['usuarioLog'] = self.request.user
        return context
    
    
class UsuarioCreateView(LoginRequiredMixin,RolRequeridoMixin,CreateView):
    model = Users
    form_class = UsersForm
    template_name = 'Usuarios/userCreate.html'
    success_url = reverse_lazy('userList')
    rol_requerido = 'Jefe de Bodega'
    login_url = 'registration/login.html'
    redirect_field_name = 'Usuarios/userCreate.html'
    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({
            "success": True,
            "message": "Usuario creada con éxito."
        })

    def form_invalid(self, form):
        return JsonResponse({
            "success": False,
            "errors": form.errors
        }, status=400)


class UsuarioUpdateView(LoginRequiredMixin,RolRequeridoMixin,UpdateView):
    model = Users
    form_class = UsersForm
    template_name = 'Usuarios/userUpdate.html'
    success_url = reverse_lazy('userList')
    rol_requerido = 'Jefe de Bodega'
    login_url = 'registration/login.html'
    redirect_field_name = 'Usuarios/userUpdate.html'
    context_object_name = 'usuario'
    def get_object(self, queryset=None):
        # Aquí obtienes el objeto usuario de la lista (basado en el id)
        return get_object_or_404(Users, pk=self.kwargs['pk'])
    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({
            "success": True,
            "message": "Usuario creada con éxito."
        })

    def form_invalid(self, form):
        return JsonResponse({
            "success": False,
            "errors": form.errors
        }, status=400)
    

class UsuarioDeleteView(LoginRequiredMixin,RolRequeridoMixin,DeleteView):
    model = Users
    template_name = 'Usuarios/userDelete.html'
    success_url = reverse_lazy('userList')
    context_object_name = 'usuario'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()  #obtenemos el objeto del usuario con la id (pk) de la URL
        context['username'] = user.username  #agrega el username al contexto para usarlo en la plantilla
        return context
    def post(self, request, *args, **kwargs):
        user = self.get_object()
        #se va a eliminar el usuario
        try:
            user.delete()
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
    rol_requerido = 'Jefe de Bodega'
    login_url = 'registration/login.html'
    redirect_field_name = 'Usuarios/userDelete.html'
    
    
class UsuarioDetailView(LoginRequiredMixin,RolRequeridoMixin,DetailView):
    model = Users
    template_name = 'Usuarios/userDetail.html'
    context_object_name = 'usuario'
    rol_requerido = 'Jefe de Bodega'
    login_url = 'registration/login.html'
    redirect_field_name = 'Usuarios/userDetail.html'

