from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from Libros.forms import LibroForm
from Libros.models import Libro
from django.urls import reverse_lazy
# Create your views here.


def base(request):
    return render(request, 'Libros/base_libros.html')


class LibroListView(ListView):
    model = Libro
    template_name = 'libros/libros_list.html'
    context_object_name = 'libros'

class LibroCreateView(CreateView):
    model = Libro
    template_name = 'libros/libros_create.html'
    form_class = LibroForm
    success_url = reverse_lazy

class LibroDeleteView(DeleteView):
    model = Libro
    template_name = 'libros/libros_delete.html'
    success_url = reverse_lazy('list')
    context_object_name = 'libros'

class LibroUpdateView(UpdateView):
    model = Libro
    template_name = 'libros/libros_update.html'
    form_class = LibroForm
    success_url = reverse_lazy('list')

class LibroDetailView(DetailView):
    model = Libro
    template_name = 'libros/libros_detail.html'
    context_object_name = 'libro'