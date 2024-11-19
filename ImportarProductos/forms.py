from django import forms

class ImportarProductosForm(forms.Form):
    archivo = forms.FileField()
