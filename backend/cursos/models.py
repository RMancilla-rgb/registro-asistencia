# registro_asistencia/backend/cursos/models.py

from django.db import models
from clientes.models import Colegio

class Curso(models.Model):
    colegio = models.ForeignKey(
        Colegio,
        on_delete=models.PROTECT,
        related_name='cursos',
        # Si prefieres que siempre se asigne un colegio, quita las dos líneas siguientes:
        null=True,
        blank=True,
    )

    CICLOS = [
        ('basica',          'Básica'),
        ('media',           'Media'),
        ('ADULTOS_BASICA',  'Educación de Adultos – Básica'),
        ('ADULTOS_MEDIA',   'Educación de Adultos – Media'),
    ]

    # Secciones A–Z
    SECCIONES = [(letra, letra) for letra in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']

    ciclo   = models.CharField(max_length=20, choices=CICLOS)
    grado   = models.PositiveSmallIntegerField(
        help_text="1–8 si es Básica; 1–4 si es Media"
    )
    seccion = models.CharField(
        max_length=1,
        choices=SECCIONES,
        default='A',
        help_text="Letra de la sección (A, B, C…)",
    )

    class Meta:
        unique_together = ('colegio', 'ciclo', 'grado', 'seccion')
        ordering = ['colegio__nombre', 'ciclo', 'grado', 'seccion']
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'

    def __str__(self):
        # Muestra: "Colegio – Básica 1° A"
        colegio_nombre = self.colegio.nombre if self.colegio else "(Sin colegio)"
        return f"{colegio_nombre} – {self.get_ciclo_display()} {self.grado}° {self.seccion}"


class Alumno(models.Model):
    nombre = models.CharField(max_length=100)
    rut    = models.CharField(max_length=12, unique=True)
    curso  = models.ForeignKey(
        Curso,
        on_delete=models.PROTECT,
        related_name='alumnos'
    )

    class Meta:
        ordering = ['curso__colegio__nombre', 'curso__ciclo', 'curso__grado', 'curso__seccion', 'nombre']
        verbose_name = 'Alumno'
        verbose_name_plural = 'Alumnos'

    def __str__(self):
        return f"{self.nombre} ({self.rut})"
