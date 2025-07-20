from django.db import models
from django.conf import settings
from cursos.models import Curso, Alumno
from clientes.models import Colegio


class Taller(models.Model):
    nombre = models.CharField(max_length=100)

    # Colegio asociado (solo para referencia directa)
    colegio = models.ForeignKey(
        Colegio,
        on_delete=models.CASCADE,
        related_name='talleres',
        null=True,
        blank=True,
        help_text="Colegio al que pertenece este taller"
    )

    # Curso al que se imparte el taller
    curso = models.ForeignKey(
        Curso,
        on_delete=models.PROTECT,
        related_name='talleres'
    )

    # Profesor encargado
    profesor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='talleres_asignados',
        limit_choices_to={'rol': 'profesor'}
    )

    # Alumnos participantes (selección múltiple)
    alumnos = models.ManyToManyField(
        Alumno,
        blank=True,
        related_name='talleres'
    )

    # Numero de sesiones
    numero_sesiones = models.PositiveIntegerField(
        'Número de sesiones planificadas',
        default=0,
        help_text='Cantidad total de días/sesiones que se espera realizar en este taller'
    )

    def __str__(self):
        return f"{self.nombre} ({self.curso})"

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Taller'
        verbose_name_plural = 'Talleres'
