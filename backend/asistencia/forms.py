from django import forms
from talleres.models import Taller
from datetime import datetime

class ReporteAsistenciaForm(forms.Form):
    taller = forms.ModelChoiceField(queryset=Taller.objects.none(), label="Taller")
    mes = forms.ChoiceField(choices=[(i, i) for i in range(1, 13)], label="Mes")
    anio = forms.ChoiceField(label="Año")

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Mostrar solo talleres accesibles según rol
        if user.rol == 'profesor':
            self.fields['taller'].queryset = user.talleres_asignados.all()
        elif user.rol == 'coordinador':
            # Coordinador puede ver talleres de sus cursos (si lo filtras, aquí simplifico)
            self.fields['taller'].queryset = Taller.objects.all()  # luego puedes mejorar filtro
        elif user.rol == 'cliente':
            self.fields['taller'].queryset = Taller.objects.all()
        elif user.rol == 'administrador':
            self.fields['taller'].queryset = Taller.objects.all()

        # Opciones de año, desde 2020 hasta actual +1
        current_year = datetime.now().year
        self.fields['anio'].choices = [(y, y) for y in range(2020, current_year + 2)]



class SubirAsistenciaExcelForm(forms.Form):
    archivo = forms.FileField(
        label="Archivo Excel de Asistencia (.xlsx)",
        help_text="Usa la plantilla oficial con celdas B1=Taller, B2=Fecha y tabla a partir de la fila 5"
    )