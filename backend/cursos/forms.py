# registro_asistencia/backend/cursos/forms.py
from django import forms
from .models import Curso, Alumno
from clientes.models import Colegio

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'
        widgets = {
            'colegio': forms.Select(attrs={'class': 'border p-2 rounded'}),
            'ciclo':   forms.Select(attrs={'class': 'border p-2 rounded'}),
            'grado':   forms.NumberInput(attrs={'class': 'border p-2 rounded', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and hasattr(user, 'rol') and user.rol == 'coordinador':
            colegio = getattr(user, 'colegio', None)
            if colegio:
                self.fields['colegio'].queryset = Colegio.objects.filter(pk=colegio.pk)
            else:
                self.fields['colegio'].queryset = Colegio.objects.none()
        else:
            self.fields['colegio'].queryset = Colegio.objects.all()

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'rut', 'curso']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'border p-2 rounded w-full'}),
            'rut': forms.TextInput(attrs={'class': 'border p-2 rounded w-full'}),
            'curso': forms.Select(attrs={'class': 'border p-2 rounded w-full'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user and hasattr(user, 'rol') and user.rol == 'coordinador':
            colegio = getattr(user, 'colegio', None)
            if colegio:
                self.fields['curso'].queryset = Curso.objects.filter(colegio=colegio)
            else:
                self.fields['curso'].queryset = Curso.objects.none()
        else:
            self.fields['curso'].queryset = Curso.objects.select_related('colegio').all()
