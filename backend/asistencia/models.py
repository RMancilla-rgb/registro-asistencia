from django.db import models
from cursos.models import Alumno
from talleres.models import Taller
from clientes.models import Colegio
from django.conf import settings

class Asistencia(models.Model):
    ESTADOS = [
        ('P', 'Presente'),
        ('F', 'Falta'),
    ]
    taller = models.ForeignKey(
        Taller, on_delete=models.CASCADE, related_name='asistencias'
    )
    alumno = models.ForeignKey(
        Alumno, on_delete=models.CASCADE, related_name='asistencias'
    )
    fecha = models.DateField(auto_now_add=True)
    estado = models.CharField(max_length=1, choices=ESTADOS)

    class Meta:
        unique_together = ('taller', 'alumno', 'fecha')
        ordering = ['-fecha', 'taller', 'alumno']

    def __str__(self):
        return f"{self.fecha} – {self.alumno} – {self.get_estado_display()}"


class SesionTaller(models.Model):
    ESTADOS = [
        ('R', 'Realizada'),
        ('F', 'Feriado'),
        ('P', 'Profesor ausente'),
        ('O', 'Otro'),
    ]
    taller       = models.ForeignKey(Taller, on_delete=models.CASCADE, related_name='sesiones')
    fecha        = models.DateField()
    estado       = models.CharField(max_length=1, choices=ESTADOS, default='R')
    motivo_extra = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('taller', 'fecha')
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.fecha} – {self.get_estado_display()} ({self.taller})"



class AsistenciaUpload(models.Model):
    colegio     = models.ForeignKey(Colegio, on_delete=models.CASCADE)
    fecha       = models.DateField()
    archivo     = models.FileField(upload_to='asistencias/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('colegio', 'fecha')
        ordering = ['-fecha']