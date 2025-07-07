# registro_asistencia/backend/cursos/models.py

from django.db import models
from clientes.models import Colegio

class Curso(models.Model):
    colegio = models.ForeignKey(
        Colegio,
        on_delete=models.PROTECT,
        related_name='cursos',
        null=True,
        blank=True,
    )
    CICLOS = [
        ('basica', 'Básica'),
        ('media',  'Media'),
        ('ADULTOS_BASICA', 'Educación de Adultos - Básica'),
        ('ADULTOS_MEDIA', 'Educación de Adultos - Media'),
    ]
    ciclo = models.CharField(max_length=20, choices=CICLOS)
    grado = models.PositiveSmallIntegerField(
        help_text="1–8 si es Básica, 1–4 si es Media"
    )

    class Meta:
        unique_together = ('colegio', 'ciclo', 'grado')
        ordering = ['colegio', 'ciclo', 'grado']

    def __str__(self):
        return f"{self.colegio} – {self.get_ciclo_display()} {self.grado}°"

class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    rut    = models.CharField(max_length=12, unique=True)
    curso  = models.ForeignKey(
        Curso, on_delete=models.PROTECT,
        related_name='alumnos'
    )

    def __str__(self):
        return f"{self.nombre} ({self.rut})"
