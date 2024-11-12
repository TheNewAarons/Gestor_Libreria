from django import forms
from .models import Libro, Author

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ('title', 'description', 'author', 'tipo', 'editorial', 'tamaño')
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'tamaño': forms.TextInput(attrs={'class': 'form-control'}),
            'editorial': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-control'}),
        }

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ('name', 'last_name')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }