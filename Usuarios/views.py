from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from Usuarios.models import Users
from Usuarios.forms import UsersForm
from django.urls import reverse_lazy
# Create your views here.

class UsuarioListView(ListView):
    model = Users
    template_name = 'Usuarios/userList.html'
    context_object_name = 'usuarios'
    
class UsuarioCreateView(CreateView):
    model = Users
    form_class = UsersForm
    template_name = 'Usuarios/userCreate.html'
    success_url = reverse_lazy('userList')

class UsuarioUpdateView(UpdateView):
    model = Users
    form_class = UsersForm
    template_name = 'Usuarios/userUpdate.html'
    success_url = reverse_lazy('userList')

class UsuarioDeleteView(DeleteView):
    model = Users
    template_name = 'Usuarios/userDelete.html'
    success_url = reverse_lazy('userList')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()  # obtiene el objeto del usuario con la id (pk) de la URL
        context['username'] = user.username  # agrega el username al contexto para usarlo en la plantilla
        return context
    
class UsuarioDetailView(DetailView):
    model = Users
    template_name = 'Usuarios/userDetail.html'
    context_object_name = 'usuario'