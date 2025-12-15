from django import forms
from .models import Bodega
from .models import ProductoBodega

class BodegasForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = ('nombre', 'direction', 'tipo_de_contenido', 'estado', 'tamaño_bodega', 'capacidad')
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre de la bodega'
            }),
            'direction': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Dirección de la bodega'
            }),
            'tipo_de_contenido': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tipo de contenido'
            }),
            'estado': forms.Select(attrs={
                'class': 'form-select'
            }),
            'tamaño_bodega': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tamaño de la bodega'
            }),
            'capacidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Capacidad de la bodega'
            })
        }

    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        direction = cleaned_data.get('direction')

        # Validar que el nombre no exista
        if Bodega.objects.filter(nombre=nombre).exists():
            self.add_error('nombre', 'Ya existe una bodega con este nombre.')

        # Validar que la dirección no exista
        if Bodega.objects.filter(direction=direction).exists():
            self.add_error('direction', 'Ya existe una bodega con esta dirección.')

        return cleaned_data

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


class RetirarProductoForm(forms.Form):
    bodega = forms.ModelChoiceField(
        queryset=Bodega.objects.all(), 
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    producto_bodega = forms.ModelChoiceField(
        queryset=ProductoBodega.objects.none(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    cantidad_retirar = forms.IntegerField(
        min_value=1, 
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese la cantidad a retirar'})
    )

    def __init__(self, *args, **kwargs):
        bodega_id = kwargs.pop('bodega_id', None)  # Capturar la bodega específica si es pasada
        super().__init__(*args, **kwargs)
        if bodega_id:
            self.fields['producto_bodega'].queryset = ProductoBodega.objects.filter(bodega_id=bodega_id)

    def clean(self):
        cleaned_data = super().clean()
        producto_bodega = cleaned_data.get('producto_bodega')  # Producto en la bodega
        cantidad_retirar = cleaned_data.get('cantidad_retirar')  # Cantidad solicitada para retirar

        if producto_bodega and cantidad_retirar:
            # Verificamos que no se retire más de lo que hay en stock en la bodega
            if cantidad_retirar > producto_bodega.bodega.nivel_stock:
                raise forms.ValidationError(
                    f'No hay suficiente stock en la bodega para retirar "{producto_bodega.producto.title}". '
                    f'Stock disponible en la bodega: {producto_bodega.bodega.nivel_stock}.'
                )

            # Verificamos que la cantidad solicitada no supere el stock del libro
            if cantidad_retirar > producto_bodega.producto.cantidad:
                raise forms.ValidationError(
                    f'No hay suficiente stock del producto "{producto_bodega.producto.title}". '
                    f'Stock disponible: {producto_bodega.producto.cantidad}.'
                )
        return cleaned_data

