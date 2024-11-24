from django.shortcuts import render
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from Bodegas.forms import BodegasForm, ProductoBodegaForm
from Bodegas.models import Bodega, ProductoBodega
from django.urls import reverse_lazy

# Create your views here.

def agregar_producto_bodega(request):
    if request.method == 'POST':
        form = ProductoBodegaForm(request.POST)
        if form.is_valid():
            # Si el formulario es válido, guardamos el producto
            producto_bodega = form.save()

            # Actualizamos el stock de la bodega
            bodega = producto_bodega.bodega
            bodega.nivel_stock += producto_bodega.cantidad  # Suma la cantidad
            bodega.save()

            # Redirigir al listado de bodegas
            return redirect('bodegas_list')
        else:
            # Si el formulario no es válido, mostramos el mensaje de error
            messages.error(request, form.errors)

    else:
        form = ProductoBodegaForm()

    return render(request, 'Bodegas/agregar_producto_bodega.html', {'form': form})



class BodegasListView(ListView):
    model = Bodega
    template_name = 'Bodegas/bodegas_list.html'
    context_object_name = 'bodegas'

class BodegasCreateView(CreateView):
    model = Bodega
    template_name = 'Bodegas/bodegas_create.html'
    form_class = BodegasForm
    success_url = reverse_lazy('bodegas_list')

class BodegasUpdateView(UpdateView):
    model = Bodega
    template_name = 'Bodegas/bodegas_update.html'
    form_class = BodegasForm
    success_url = reverse_lazy('bodegas_list')

class BodegasDeleteView(DeleteView):
    model = Bodega
    template_name = 'Bodegas/bodegas_delete.html'
    context_object_name = 'bodega'
    success_url = reverse_lazy('bodegas_list')

class BodegasDetailView(DetailView):
    model = Bodega
    template_name = 'Bodegas/bodegas_detail.html'
    context_object_name = 'bodega'
