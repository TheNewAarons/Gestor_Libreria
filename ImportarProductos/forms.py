from django import forms

class ImportarProductosForm(forms.Form):
    archivo = forms.FileField(
        label='Seleccione el archivo Excel',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx, .xls',
        })
    )

    def clean_archivo(self):
        archivo = self.cleaned_data['archivo']
        if not archivo.name.endswith(('.xlsx', '.xls')):
            raise forms.ValidationError('El archivo debe ser un Excel (.xlsx o .xls)')
        return archivo
