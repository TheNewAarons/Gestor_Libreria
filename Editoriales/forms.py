from django import forms
from Editoriales.models import Editorial

class EditorialForm(forms.ModelForm):
    class Meta:
        model = Editorial
        fields = ('name', 'address', 'phone')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control text-color'}),
            'address': forms.TextInput(attrs={'class': 'form-control text-color'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control text-color'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.label_class = 'label-custom' 