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