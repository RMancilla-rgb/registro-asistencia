from django import forms
from .models import Dueno, Colegio
from usuarios.models import Usuario

class DuenoForm(forms.ModelForm):
    class Meta:
        model = Dueno
        fields = ['nombre', 'user']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'border p-2 rounded'}),
            'user': forms.Select(attrs={'class': 'border p-2 rounded'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = Usuario.objects.filter(rol='cliente')

class ColegioForm(forms.ModelForm):
    class Meta:
        model = Colegio
        fields = ['nombre', 'direccion', 'dueno', 'coordinador']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'border p-2 rounded'}),
            'direccion': forms.TextInput(attrs={'class': 'border p-2 rounded'}),
            'dueno': forms.Select(attrs={'class': 'border p-2 rounded'}),
            'coordinador': forms.Select(attrs={'class': 'border p-2 rounded'}),
        }
