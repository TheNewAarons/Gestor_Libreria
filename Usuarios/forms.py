from django import forms

from Usuarios.models import Users

ROLE_CHOICES = [
    ('bodeguero', 'Bodeguero'),
    ('autor', 'Autor')
]

class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ('username', 'email', 'password', 'rol')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control text-color'}),
            'email': forms.EmailInput(attrs={'class': 'form-control text-color'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control '}),
            'rol': forms.Select(attrs={'class': 'form-control '}, choices=ROLE_CHOICES),
        }
