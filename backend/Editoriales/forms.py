import re
from django import forms
from Editoriales.models import Editorial

class EditorialForm(forms.ModelForm):
    class Meta:
        model = Editorial
        fields = ('name', 'address', 'phone')
        error_messages = {
            'name' :{
                'required' : 'Nombre es obligatorio',
                'unique' : 'Nombre ya fue registrado',
                'invalid' : 'Nombre no invalido para registrar'
            },
            'address' :{
                'required' : 'Direccion es obligatoria',
                'unique' : 'Direccion ya fue registrado',
                'invalid' : 'Direccion no invalido para registrar'
            },
            'phone' :{
                'required' : 'El telefono es obligatorio'
            }
            
        }
        widgets = {
            'name': forms.TextInput(attrs={'id' : 'id_name','class': 'form-control text-color'}),
            'address': forms.TextInput(attrs={'id' : 'id_address','class': 'form-control text-color' }),
            'phone': forms.TextInput(attrs={'id': 'phone_number', 'class': 'form-control text-color'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_class = 'label-custom' 
    
    #validamos la existencia del nombre de la editorial dentro del proyecto
    def clean_name(self):
            name = self.cleaned_data.get("name")
            if not name:  # Verificamos que el teléfono no esté vacío
                raise forms.ValidationError("El nombre de la editorial es obligatorio")
            if Editorial.objects.filter(name=name).exists():
                raise forms.ValidationError("Este nombre de la Editorial ya está registrado.")
            return name
    #validamos la existencia de la direccion dentro del proyecto
    def clean_address(self):
            address = self.cleaned_data.get("address")
            if not address:  # Verificamos que el teléfono no esté vacío
                raise forms.ValidationError("La direccion de la editorial es obligatorio")
            if Editorial.objects.filter(address=address).exists():
                raise forms.ValidationError("La direccion que usted selecciono ya fue asociada a una editorial")
            return address
    #validaremos el numero de la editorial
    def clean_phone(self):
            phone = self.cleaned_data.get("phone")
            if not phone: 
                raise forms.ValidationError("El teléfono es obligatorio")
            if phone: #para eliminar espacios
                phone = "".join(phone.split())
                if Editorial.objects.filter(phone=phone).exists():
                    raise forms.ValidationError("El numero que se ha ingresado ya fue asociado a una editorial")
                if len(phone) != 9:
                    raise forms.ValidationError('El telefono ingresado debe tener 9 caracteres')
            return phone
    
    # se hizo esta funcion para validar los campos vacios hay que ver el posible error se tuvo que recurrir a validar en el js
    #def clean(self):
    #    try:
    #        cleaned_data = super().clean()
    #        name = cleaned_data.get("name")
    #        address = cleaned_data.get("address")
    #        phone = cleaned_data.get("phone")

    #        print(f"Nombre: {name}, Dirección: {address}, Teléfono: {phone}")

    #        if not name and not address and not phone:
    #            raise forms.ValidationError("Debes completar al menos uno de los campos: nombre, dirección o teléfono")
            
    #        return cleaned_data
    #    except Exception as e:
    #        print(f"Error inesperado: {e}")
    #        raise forms.ValidationError("Error inesperado en la validación.")