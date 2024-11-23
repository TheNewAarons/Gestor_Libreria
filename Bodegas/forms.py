from django import forms
from .models import Bodega
from .models import ProductoBodega

class BodegasForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = ('nombre', 'direction', 'tipo_de_contenido', 'estado', 'tamaño_bodega', 'capacidad')
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la bodega'}),
            'direction': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección de la bodega'}),
            'tipo_de_contenido': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'tamaño_bodega': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Tamaño de la bodega'}),
            'capacidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Capacidad de la bodega'}),
        }

class ProductoBodegaForm(forms.ModelForm):
    class Meta:
        model = ProductoBodega
        fields = ['producto', 'bodega', 'cantidad']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'bodega': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')  # El producto seleccionado
        cantidad = cleaned_data.get('cantidad')  # La cantidad solicitada
        bodega = cleaned_data.get('bodega')  # La bodega seleccionada

        if producto and cantidad:
            # Verificar que no haya más cantidad solicitada que la disponible del producto
            if cantidad > producto.cantidad:
                raise forms.ValidationError(
                    f'No hay suficiente stock del producto "{producto.title}". Stock disponible: {producto.cantidad}.'
                )

        if bodega and cantidad:
            # Verificar que no se exceda la capacidad de la bodega
            if cantidad + bodega.nivel_stock > bodega.capacidad:
                raise forms.ValidationError(
                    f'La cantidad solicitada excede la capacidad de la bodega "{bodega.nombre}". Capacidad máxima: {bodega.capacidad}.'
                )

        return cleaned_data
