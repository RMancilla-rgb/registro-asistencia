from django.db import models
from usuarios.models import Usuario

class Dueno(models.Model):
    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre"
    )
    user = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='dueno',
        null=True,  # 👈 permite crear la migración sin error
        blank=True
    )

    def __str__(self):
        return self.nombre

class Colegio(models.Model):
    nombre = models.CharField(
        max_length=200,
        verbose_name="Nombre"
    )
    direccion = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Dirección"
    )
    dueno = models.ForeignKey(
        Dueno,
        on_delete=models.CASCADE,
        related_name='colegios',
        verbose_name="Dueño"
    )
    coordinador = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        limit_choices_to={'rol': 'coordinador'},
        related_name='colegios_asignados',
        verbose_name="Coordinador"
    )

    def __str__(self):
        return f"{self.nombre} ({self.dueno})"
