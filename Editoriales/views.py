from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from Libros.models import Editorial
from Editoriales.forms import EditorialForm
from django.urls import reverse_lazy
# Create your views here.

class EditorialListView(ListView):
    model = Editorial
    template_name = 'Editoriales/editorialList.html'
    context_object_name = 'editoriales'

class EditorialCreateView(CreateView):
    model = Editorial
    form_class = EditorialForm
    template_name = 'Editoriales/editorialCreate.html'
    success_url  = reverse_lazy('editorialList')

class EditorialDeleteView(DeleteView):
    model = Editorial
    template_name = 'Editoriales/editorialDelete.html'
    success_url = reverse_lazy('editorialList')

class EditorialUpdateView(UpdateView):
    model = Editorial
    form_class = EditorialForm
    template_name = 'Editoriales/editorialUpdate.html'
    success_url = reverse_lazy('editorialList')