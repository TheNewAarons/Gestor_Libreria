from django import forms
from Usuarios.models import Users
from .models import Libro

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ('title', 'description', 'author', 'tipo', 'editorial', 'tamaño', 'portada')
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'editorial': forms.Select(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
            'tamaño': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'portada': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar usuarios con rol "autor"
        self.fields['author'].queryset = Users.objects.filter(rol='autor')  # Ajusta el nombre del campo del rol

