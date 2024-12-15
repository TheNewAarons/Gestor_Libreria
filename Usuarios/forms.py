from django import forms
from django.contrib.auth.forms import UserCreationForm
from Usuarios.models import Users
from Usuarios.models import Users

class UsersForm(UserCreationForm):
    error_messages = {
        'password_mismatch' : 'Las contraseñas no coinciden'
    }
    password1 = forms.CharField(
        widget= forms.PasswordInput(attrs={'class' : 'form-control'}),
        error_messages={
            'requerid' : 'La contraseña debe ser obligatoria',
            'invalid' : 'La contraseña no es valida'
        }
    )
    password2 = forms.CharField(
        widget= forms.PasswordInput(attrs={'class' : 'form-control'}),
        error_messages={
            'requerid' : 'Se debe confirmar la contraseña',
            'invalid' : 'La confirmacion no es valida'
        }
    )
    class Meta:
        model = Users
        fields = ('username', 'email', 'password1', 'password2', 'rol')
        error_menssages ={
            'username':{
                'required' : 'El nombre de usuario debe ser obligatorio',
                'unique' : 'El usuario ya fue registrado en el sistema'
            },
            'email':{
                'required' : 'El correo debe ser obligatorio',
                'unique' : 'El correo ya ha sido registrado en el sistema'
            }
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'rol': forms.Select(attrs={'class': 'form-control'}),
        }
    def clean_username(self):
            username = self.cleaned_data.get("username")
            if Users.objects.filter(username=username).exists():
                raise forms.ValidationError("Este nombre de usuario ya está registrado.")
            return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Users.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2
    
            

        
