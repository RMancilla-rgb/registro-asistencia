# talleres/forms.py

from django import forms
from .models import Taller
from cursos.models import Curso
from cursos.models import Alumno


class TallerForm(forms.ModelForm):
    class Meta:
        model = Taller
        fields = [
            'curso',
            'nombre',
            'profesor',
            'alumnos',
            'numero_sesiones',    # <-- aquí
        ]
        widgets = {
            'numero_sesiones': forms.NumberInput(attrs={
                'class': 'w-full px-3 py-2 border rounded',
                'min': 0,
            }),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Filtrar cursos si es coordinador
        if user and user.rol == 'coordinador':
            colegio = getattr(user, 'colegio', None)
            self.fields['curso'].queryset = Curso.objects.filter(colegio=colegio)
        else:
            self.fields['curso'].queryset = Curso.objects.all()

        self.fields['alumnos'].queryset = Alumno.objects.none()
