# registro_asistencia/backend/cursos/forms.py

from django import forms
from .models import Curso, Alumno
from clientes.models import Colegio

class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = ['colegio', 'ciclo', 'grado', 'seccion']
        widgets = {
            'colegio': forms.Select(attrs={'class': 'border p-2 rounded'}),
            'ciclo':   forms.Select(attrs={'class': 'border p-2 rounded'}),
            'grado':   forms.NumberInput(attrs={'class': 'border p-2 rounded', 'min': 1}),
            'seccion': forms.Select(attrs={'class': 'border p-2 rounded'}),
        }

    def __init__(self, *args, **kwargs):
        # 1) Extraemos el user de kwargs, para no pasarlo al form base
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # 2) Si es coordinador, limitamos colegios a su propio colegio
        if user and getattr(user, 'rol', None) == 'coordinador':
            self.fields['colegio'].queryset = Colegio.objects.filter(id=user.colegio_id)

        # 3) Lógica para filtrar secciones ya usadas
        # Obtenemos valores actuales o iniciales
        colegio = self.initial.get('colegio') or (self.instance.colegio if self.instance.pk else None)
        ciclo   = self.initial.get('ciclo')   or getattr(self.instance, 'ciclo', None)
        grado   = self.initial.get('grado')   or getattr(self.instance, 'grado', None)

        if colegio and ciclo and grado:
            usadas = Curso.objects.filter(
                colegio=colegio, ciclo=ciclo, grado=grado
            ).values_list('seccion', flat=True)
            disponibles = [
                (letra, letra)
                for letra, _ in Curso.SECCIONES
                if letra not in usadas or letra == getattr(self.instance, 'seccion', None)
            ]
            self.fields['seccion'].choices = disponibles


class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombre', 'rut', 'curso']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'border p-2 rounded'}),
            'rut':    forms.TextInput(attrs={'class': 'border p-2 rounded'}),
            'curso':  forms.Select(attrs={'class': 'border p-2 rounded'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Si es coordinador, sólo dejar cursos de su colegio
        if user and getattr(user, 'rol', None) == 'coordinador':
            self.fields['curso'].queryset = Curso.objects.filter(colegio=user.colegio)

