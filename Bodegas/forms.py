from django import forms
from .models import Bodega
from .models import ProductoBodega

class BodegasForm(forms.ModelForm):
    class Meta:
        model = Bodega
        fields = ('nombre', 'direction', 'estado', 'tamaño_bodega', 'tipo_de_contenido')
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la bodega'}),
            'direction': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección de la bodega'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'tamaño_bodega': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_de_contenido': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ProductoBodegaForm(forms.ModelForm):
    class Meta:
        model = ProductoBodega
        fields = ['producto', 'bodega', 'cantidad']