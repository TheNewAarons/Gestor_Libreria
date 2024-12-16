import os
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.shortcuts import render, redirect
from Bodegas.forms import BodegasForm, ProductoBodegaForm, RetirarProductoForm
from Bodegas.models import Bodega, ProductoBodega
from django.urls import reverse_lazy
from django.db.models import Sum
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO

from GestorLibreria import settings

# Create your views here.
class RolRequeridoMixin(UserPassesTestMixin):
    rol_requerido = 'Jefe de Bodega'

    def test_func(self):
        return self.request.user.rol == self.rol_requerido

    def handle_no_permission(self):
        return redirect('no_autorizado')

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
    # Obtener todas las bodegas con estado 'OC'
    bodegas = Bodega.objects.filter(estado='OC')
    context = {
        'bodegas': bodegas,
        'productos_bodega': []
    }

    # Verificar si se seleccionó una bodega
    bodega_id = request.GET.get('bodega')
    if bodega_id:
        try:
            bodega = Bodega.objects.get(id=bodega_id)
            productos_bodega = ProductoBodega.objects.filter(bodega=bodega)
            context.update({
                'productos_bodega': productos_bodega,
                'bodega_seleccionada': bodega
            })
        except Bodega.DoesNotExist:
            messages.error(request, 'Bodega no encontrada')

    # Procesar el retiro de productos
    if request.method == 'POST':
        try:
            bodega = Bodega.objects.get(id=request.POST.get('bodega'))
            producto_bodega = ProductoBodega.objects.get(id=request.POST.get('producto'))
            cantidad = int(request.POST.get('cantidad'))

            if cantidad > producto_bodega.cantidad:
                messages.error(request, f'No hay suficiente stock. Stock disponible: {producto_bodega.cantidad}')
            else:
                # Actualizar ProductoBodega
                producto_bodega.cantidad -= cantidad
                if producto_bodega.cantidad == 0:
                    producto_bodega.delete()
                else:
                    producto_bodega.save()

                # Actualizar Bodega
                bodega.nivel_stock -= cantidad
                if bodega.nivel_stock == 0:
                    bodega.estado = 'VA'
                bodega.save()

                # Actualizar Producto
                producto = producto_bodega.producto
                producto.cantidad += cantidad
                producto.save()
                
                messages.success(request, 'Producto retirado exitosamente')
                return redirect('bodegas_list')

        except Exception as e:
            messages.error(request, f'Error al retirar producto: {str(e)}')

    return render(request, 'bodegas/retirar_producto_bodega.html', context)

def mover_producto(request):
    # Obtener bodegas que tienen productos con cantidad mayor a 0
    bodegas_origen = Bodega.objects.filter(
        id__in=ProductoBodega.objects.values('bodega_id').annotate(total=Sum('cantidad')).filter(total__gt=0).values('bodega_id')
    )
    bodegas_destino = Bodega.objects.exclude(estado='MN')
    productos = None
    bodega_seleccionada = None

    if 'bodega_origen' in request.GET:
        bodega_id = request.GET.get('bodega_origen')
        bodega_seleccionada = Bodega.objects.get(id=bodega_id)
        productos = ProductoBodega.objects.filter(bodega=bodega_seleccionada, cantidad__gt=0)

    if request.method == 'POST':
        try:
            bodega_origen_id = request.POST.get('bodega_origen')
            bodega_destino_id = request.POST.get('bodega_destino')
            producto_id = request.POST.get('producto')
            cantidad = int(request.POST.get('cantidad', 0))

            if not all([bodega_origen_id, bodega_destino_id, producto_id, cantidad]):
                messages.error(request, 'Todos los campos son requeridos')
                return redirect('mover_producto')

            bodega_origen = Bodega.objects.get(id=bodega_origen_id)
            bodega_destino = Bodega.objects.get(id=bodega_destino_id)

            if bodega_origen.estado != 'OC':
                messages.error(request, 'La bodega de origen debe estar ocupada')
                return redirect('mover_producto')

            if bodega_destino.estado == 'MN':
                messages.error(request, 'No se puede mover productos a una bodega en mantenimiento')
                return redirect('mover_producto')

            if bodega_origen_id == bodega_destino_id:
                messages.error(request, 'Las bodegas deben ser diferentes')
                return redirect('mover_producto')

            # Usar aggregate para sumar las cantidades de productos duplicados
            producto_bodega_total = ProductoBodega.objects.filter(
                bodega_id=bodega_origen_id, 
                producto_id=producto_id
            ).aggregate(
                total_cantidad=Sum('cantidad')
            )['total_cantidad'] or 0

            if producto_bodega_total == 0:
                messages.error(request, 'No hay stock disponible en la bodega de origen')
                return redirect('mover_producto')

            if cantidad <= 0:
                messages.error(request, 'La cantidad debe ser mayor a 0')
                return redirect('mover_producto')
                
            if cantidad > producto_bodega_total:
                messages.error(request, f'Stock insuficiente. Disponible: {producto_bodega_total}')
                return redirect('mover_producto')

            # Obtener todos los registros duplicados
            productos_bodega = ProductoBodega.objects.filter(
                bodega_id=bodega_origen_id, 
                producto_id=producto_id
            ).order_by('id')

            # Consolidar en el primer registro y eliminar los demás
            producto_bodega = productos_bodega.first()
            producto_bodega.cantidad = producto_bodega_total
            productos_bodega.exclude(id=producto_bodega.id).delete()

            # Crear o actualizar el producto en la bodega de destino
            producto_destino, created = ProductoBodega.objects.get_or_create(
                bodega=bodega_destino,
                producto_id=producto_id,
                defaults={'cantidad': 0}
            )

            # Realizar el movimiento
            producto_bodega.cantidad -= cantidad
            producto_destino.cantidad += cantidad
            
            producto_bodega.save()
            producto_destino.save()

            # Actualizar nivel_stock de ambas bodegas
            bodega_origen.nivel_stock = ProductoBodega.objects.filter(bodega=bodega_origen).aggregate(Sum('cantidad'))['cantidad__sum'] or 0
            bodega_destino.nivel_stock = ProductoBodega.objects.filter(bodega=bodega_destino).aggregate(Sum('cantidad'))['cantidad__sum'] or 0
            
            # Actualizar estados basados en nivel_stock
            if bodega_origen.nivel_stock == 0:
                bodega_origen.estado = 'VA'
            if bodega_destino.nivel_stock > 0:
                bodega_destino.estado = 'OC'
            
            bodega_origen.save()
            bodega_destino.save()
            usuario = request.user
            html_content = render_to_string('Bodegas/movimiento_pdf.html', {
                'bodega_origen': bodega_origen,
                'bodega_destino': bodega_destino,
                'producto': ProductoBodega.objects.get(id=producto_id),
                'cantidad': cantidad,
                'username': usuario.username,
                'rol': usuario.rol
            })

            # Ruta temporal para almacenar el PDF
            pdf_filename = f"movimiento_{bodega_destino.nombre}_{ProductoBodega.objects.get(id=producto_id).producto.title}.pdf"
        
            # Ruta para almacenar el PDF
            pdf_path = os.path.join(settings.MEDIA_ROOT, 'pdfs', pdf_filename)
            
            print(f"Generando PDF en: {pdf_path}")  # Debugging: verificar la ruta de destino del PDF
            
            # Crear el archivo PDF
            with open(pdf_path, "wb") as pdf_file:
                pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)

            # Verificar si hubo errores al generar el PDF
            if pisa_status.err:
                print("Error al generar el PDF:", pisa_status.err)  # Debugging: información del error
                return JsonResponse({"success": False, "message": "Error al generar el PDF"})
            
            # Construir la URL pública para acceder al archivo PDF
            pdf_url = f"{settings.MEDIA_URL}pdfs/{pdf_filename}"
            print(f"PDF generado en: {pdf_url}")  # Debugging: verificar la URL generada
            
            return JsonResponse({
                "success": True,
                "message": "Movimiento realizado exitosamente",
                "pdf_url": pdf_url.replace("\\", "/"),  # Reemplazar \ por /
            })
        
        except Exception as e:
            print(f"Error en el proceso: {str(e)}")  # Debugging: Ver error general
            return JsonResponse({"success": False, "message": f"Ocurrió un problema: {str(e)}"})

    context = {
        'bodegas_origen': bodegas_origen,
        'bodegas_destino': bodegas_destino,
        'productos': productos,
        'bodega_seleccionada': bodega_seleccionada
    }
    return render(request, 'bodegas/mover_producto_entre_bodega.html', context)

def get_productos_bodega(request):
    try:
        bodega_id = request.GET.get('bodega_id')
        if not bodega_id:
            return JsonResponse({'error': 'Bodega ID es requerido'}, status=400)
            
        productos = ProductoBodega.objects.filter(
            bodega_id=bodega_id,
            cantidad__gt=0
        ).select_related('producto')
        
        productos_list = [{
            'id': prod.producto.id,
            'nombre': f"{prod.producto.title} (Stock: {prod.cantidad})"
        } for prod in productos]
        
        return JsonResponse({'productos': productos_list})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

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

def eliminar_bodegas_view(request):
    # Filtrar bodegas que están vacías y no están ocupadas
    bodegas_para_eliminar = Bodega.objects.filter(estado='VA', nivel_stock=0)

    if request.method == 'POST':
        bodega_id = request.POST.get('bodega_id')
        bodega = get_object_or_404(Bodega, id=bodega_id, estado='VA', nivel_stock=0)
        bodega.delete()
        messages.success(request, 'Bodega eliminada exitosamente')
        return redirect('eliminar_bodegas')

    return render(request, 'bodegas/eliminar_bodegas.html', {'bodegas': bodegas_para_eliminar})

def bodegas_detail_list(request):
    bodegas = Bodega.objects.all()
    detalles_bodegas = []
    
    for bodega in bodegas:
        productos = ProductoBodega.objects.filter(bodega=bodega, cantidad__gt=0)
        detalles_bodegas.append({
            'bodega': bodega,
            'productos': productos,
            'total_productos': sum(p.cantidad for p in productos)
        })
    
    return render(request, 'bodegas/bodegas_detail_list.html', {
        'detalles_bodegas': detalles_bodegas
    })

def editar_bodegas_list(request):
    bodegas = Bodega.objects.all()
    return render(request, 'bodegas/editar_bodegas_list.html', {'bodegas': bodegas})

def editar_bodega(request, pk):
    bodega = get_object_or_404(Bodega, pk=pk)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        
        # Verificar si el nombre o dirección ya existen en otras bodegas
        if Bodega.objects.exclude(pk=pk).filter(nombre=nombre).exists():
            messages.error(request, 'Ya existe una bodega con este nombre')
            return redirect('editar_bodega', pk=pk)
            
        if Bodega.objects.exclude(pk=pk).filter(direccion=direccion).exists():
            messages.error(request, 'Ya existe una bodega con esta dirección')
            return redirect('editar_bodega', pk=pk)
            
        bodega.nombre = nombre
        bodega.direccion = direccion
        bodega.save()
        
        messages.success(request, 'Bodega actualizada exitosamente')
        return redirect('editar_bodegas_list')
        
    return render(request, 'bodegas/editar_bodega.html', {'bodega': bodega})

class BodegaEstadoListView(RolRequeridoMixin, ListView):
    model = Bodega
    template_name = 'bodegas/bodega_estado_list.html'
    context_object_name = 'bodegas'
    rol_requerido = 'Jefe de Bodega'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for bodega in context['bodegas']:
            bodega.productos_count = bodega.productos.count()
        return context

class BodegaEstadoUpdateView(RolRequeridoMixin, UpdateView):
    model = Bodega
    template_name = 'bodegas/bodega_estado_update.html'
    fields = ['estado']
    success_url = reverse_lazy('bodega_estado_list')
    rol_requerido = 'Jefe de Bodega'

    def form_valid(self, form):
        messages.success(self.request, 'Estado de bodega actualizado exitosamente.')
        return super().form_valid(form)