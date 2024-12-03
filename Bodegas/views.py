from django.contrib import messages
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from Bodegas.forms import BodegasForm, ProductoBodegaForm, RetirarProductoForm
from Bodegas.models import Bodega, ProductoBodega
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

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
        bodega.estado = 'VA'  # Bodega vacía
    else:
        bodega.estado = 'OC'  # Bodega ocupada
    bodega.save()





def agregar_producto_bodega(request):
    if request.method == 'POST':
        form = ProductoBodegaForm(request.POST)
        if form.is_valid():
            producto_bodega = form.save(commit=False)
            libro = producto_bodega.producto  # Relación con el producto (libro)
            bodega = producto_bodega.bodega  # Relación con la bodega

            # Verificamos si hay suficiente stock del libro
            if producto_bodega.cantidad > libro.cantidad:
                messages.error(request, f'No hay suficiente stock disponible del producto "{libro.title}". Stock disponible: {libro.cantidad}')
                return redirect('agregar_producto_bodega')

            # Actualizamos el stock del libro: restamos la cantidad que se va a agregar a la bodega
            libro.cantidad -= producto_bodega.cantidad
            libro.save()

            # Actualizamos el nivel de stock de la bodega: aumentamos la cantidad que se va a agregar a la bodega
            bodega.nivel_stock += producto_bodega.cantidad
            bodega.save()

            # Llamamos a la función para actualizar el estado de la bodega (si es necesario)
            actualizar_estado_bodega(bodega)

            # Guardamos la relación entre el libro y la bodega
            producto_bodega.save()
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
            libro = producto_bodega.producto  # Relación con el libro
            bodega = producto_bodega.bodega  # Relación con la bodega

            # Verificamos que hay suficiente stock en la bodega
            if producto_bodega.cantidad > bodega.nivel_stock:
                messages.error(request, f'No hay suficiente stock en la bodega para retirar el producto "{libro.title}". Stock disponible en la bodega: {bodega.nivel_stock}')
                return redirect('retirar_producto_bodega')

            # Verificamos que el libro tiene suficiente cantidad disponible
            if producto_bodega.cantidad > libro.cantidad:
                messages.error(request, f'No hay suficiente stock del producto "{libro.title}". Stock disponible: {libro.cantidad}')
                return redirect('retirar_producto_bodega')

            # Actualizamos el stock del libro: aumentamos la cantidad de producto disponible en el libro
            libro.cantidad += producto_bodega.cantidad
            libro.save()

            # Actualizamos el nivel de stock de la bodega: restamos la cantidad que se retira
            bodega.nivel_stock -= producto_bodega.cantidad
            bodega.save()

            # Llamamos a la función para actualizar el estado de la bodega (si es necesario)
            actualizar_estado_bodega(bodega)

            producto_bodega.save()  # Guardamos la relación entre el libro y la bodega
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





class BodegasCreateView(RolRequeridoMixin,LoginRequiredMixin,CreateView):
    model = Bodega
    template_name = 'Bodegas/bodegas_create.html'
    form_class = BodegasForm
    success_url = reverse_lazy('bodegas_list')
    rol_requerido = 'Jefe de Bodega'
    login_url = 'registration/login.html'
    redirect_field_name = 'Libreria/Base_Modulos.html'





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
