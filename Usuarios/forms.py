from django import forms
from django.contrib.auth.forms import UserCreationForm #para poder implementar boostrar al form de creacion predeterminado de django
from Usuarios.models import Users

class UsersForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ('username', 'email', 'password1', 'password2' , 'rol')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }

