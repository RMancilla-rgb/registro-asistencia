from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.decorators import user_passes_test



ROLES = [
    ('administrador', 'Administrador'),
    ('coordinador', 'Coordinador'),
    ('profesor', 'Profesor'),
    ('cliente', 'Cliente'),
    ('supervisor', 'Supervisor'),
]

class Usuario(AbstractUser):
    rol = models.CharField(max_length=30, choices=ROLES)
    colegio = models.ForeignKey(
        'clientes.Colegio',  # <-- usar string en lugar del import directo
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios'
    )


def role_required(role):
    """
    Decorador para proteger vistas según rol.
    Uso:
        @login_required
        @role_required('coordinador')
        def mi_vista(request):
            ...
    """
    def check(user):
        return user.is_authenticated and user.rol == role
    return user_passes_test(check)
