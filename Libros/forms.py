from django import forms
from Usuarios.models import Users
from .models import Libro

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ('title', 'description', 'author', 'tipo', 'editorial', 'tamaño','cantidad', 'portada')
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'editorial': forms.Select(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'tamaño': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'portada': forms.ClearableFileInput(attrs={'class': 'form-control','type' : 'file', 'id' : 'formFile'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar usuarios con rol "autor"
        self.fields['author'].queryset = Users.objects.filter(rol='autor')  # Ajusta el nombre del campo del rol




class LibroFormPublicar(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['title', 'tipo', 'editorial', 'description', 'portada']  # Campos que se usarán
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe el título'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'editorial': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Escribe la descripción'}),
            'portada': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }