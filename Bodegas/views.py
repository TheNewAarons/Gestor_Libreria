from django.shortcuts import render
from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from Bodegas.forms import BodegasForm, ProductoBodegaForm, RetirarProductoForm
from Bodegas.models import Bodega, ProductoBodega
from django.urls import reverse_lazy

# Create your views here.

def agregar_producto_bodega(request):
    if request.method == 'POST':
        form = ProductoBodegaForm(request.POST)
        if form.is_valid():
            # Guardamos el producto en la bodega
            producto_bodega = form.save()

            # Actualizamos el stock de la bodega
            bodega = producto_bodega.bodega
            bodega.nivel_stock += producto_bodega.cantidad  # Actualizamos el stock de la bodega
            bodega.save()

            # Si es necesario, actualizamos la cantidad del libro en el modelo Libro
            producto_bodega.producto.cantidad -= producto_bodega.cantidad  # Reducimos la cantidad del producto
            producto_bodega.producto.save()

            # Redirigir al listado de bodegas
            return redirect('bodegas_list')
        else:
            # Si el formulario no es válido, mostramos el mensaje de error
            messages.error(request, form.errors)
    else:
        form = ProductoBodegaForm()

    return render(request, 'Bodegas/agregar_producto_bodega.html', {'form': form})




def retirar_producto_bodega(request):
    if request.method == 'POST':
        form = ProductoBodegaForm(request.POST)
        if form.is_valid():
            # Extraemos los datos del formulario
            bodega = form.cleaned_data['bodega']
            producto = form.cleaned_data['producto']
            cantidad_retirar = form.cleaned_data['cantidad']

            # Validamos si la cantidad solicitada es mayor al stock disponible en la bodega
            try:
                producto_bodega = ProductoBodega.objects.get(bodega=bodega, producto=producto)

                if producto_bodega.cantidad >= cantidad_retirar:
                    # Reducimos la cantidad en la bodega
                    producto_bodega.cantidad -= cantidad_retirar
                    producto_bodega.save()

                    # Actualizamos el stock de la bodega
                    bodega.nivel_stock -= cantidad_retirar
                    bodega.save()

                    # Aumentamos la cantidad del producto en el inventario
                    producto.cantidad += cantidad_retirar
                    producto.save()

                    messages.success(request, f'Se han retirado {cantidad_retirar} unidades de {producto.title}.')
                    return redirect('bodegas_list')

                else:
                    messages.error(request, f'No hay suficiente stock del producto "{producto.title}". Stock disponible: {producto_bodega.cantidad}.')
            except ProductoBodega.DoesNotExist:
                messages.error(request, 'El producto no está disponible en esta bodega.')

        else:
            messages.error(request, 'Por favor, corrija los errores en el formulario.')

    else:
        form = ProductoBodegaForm()

    return render(request, 'Bodegas/retirar_producto_bodega.html', {'form': form})





class BodegasListView(ListView):
    model = Bodega
    template_name = 'Bodegas/bodegas_list.html'
    context_object_name = 'bodegas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Añadimos los productos de cada bodega al contexto
        context['productos_bodega'] = ProductoBodega.objects.all()  # O filtrado según lo necesites
        return context

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
