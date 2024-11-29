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



def bodegas_list(request):
    search_query = request.GET.get('search', '')  # Capturamos el parámetro 'search'
    if search_query:
        bodegas = Bodega.objects.filter(nombre__icontains=search_query)  # Filtra por nombre que contenga el texto
    else:
        bodegas = Bodega.objects.all()  # Muestra todas las bodegas si no hay búsqueda

    return render(request, 'Bodegas/bodegas_list.html', {'bodegas': bodegas})





def actualizar_estado_bodega(bodega):
    """
    Actualiza el estado de la bodega basado en su nivel de stock.
    - Si el nivel de stock es 0, cambia el estado a 'Bacio' (BA).
    - Si el nivel de stock es mayor a 0, cambia el estado a 'Ocupado' (OC).
    """
    if bodega.nivel_stock == 0:
        bodega.estado = 'BA'  # Bodega vacía
    else:
        bodega.estado = 'OC'  # Bodega ocupada
    bodega.save()





def agregar_producto_bodega(request):
    if request.method == 'POST':
        form = ProductoBodegaForm(request.POST)
        if form.is_valid():
            producto_bodega = form.save()
            bodega = producto_bodega.bodega

            # Actualizamos el nivel de stock
            bodega.nivel_stock += producto_bodega.cantidad
            bodega.save()

            # Llamamos a la función para actualizar el estado de la bodega
            actualizar_estado_bodega(bodega)

            return redirect('bodegas_list')
        else:
            messages.error(request, form.errors)
    else:
        form = ProductoBodegaForm()

    return render(request, 'Bodegas/agregar_producto_bodega.html', {'form': form})







def retirar_producto_bodega(request):
    if request.method == 'POST':
        form = ProductoBodegaForm(request.POST)
        if form.is_valid():
            producto_bodega = form.save(commit=False)
            bodega = producto_bodega.bodega

            # Verificamos que hay suficiente stock antes de retirar
            if producto_bodega.cantidad > bodega.nivel_stock:
                messages.error(request, 'No hay suficiente stock en la bodega.')
                return redirect('retirar_producto_bodega')

            # Actualizamos el nivel de stock
            bodega.nivel_stock -= producto_bodega.cantidad
            bodega.save()

            # Llamamos a la función para actualizar el estado de la bodega
            actualizar_estado_bodega(bodega)

            producto_bodega.save()
            return redirect('bodegas_list')
        else:
            messages.error(request, form.errors)
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
