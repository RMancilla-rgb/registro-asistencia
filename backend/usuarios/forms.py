# backend/usuarios/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Usuario
from clientes.models import Colegio
from django.utils.safestring import mark_safe

class UsuarioCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'rol', 'colegio', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class':'border p-2 rounded'}),
            'email':    forms.EmailInput(attrs={'class':'border p-2 rounded'}),
            'rol':      forms.Select(attrs={'class':'border p-2 rounded'}),
        }

class UsuarioChangeForm(UserChangeForm):
    password = None  # <- esto elimina el campo de la vista

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'rol', 'colegio']
        widgets = {
            'username': forms.TextInput(attrs={'class':'border p-2 rounded'}),
            'email':    forms.EmailInput(attrs={'class':'border p-2 rounded'}),
            'rol':      forms.Select(attrs={'class':'border p-2 rounded'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rol'].choices = [('administrador', 'Administrador'), ('coordinador', 'Coordinador'),
                                      ('profesor', 'Profesor'), ('cliente', 'Cliente'), ('supervisor', 'Supervisor')]

        if 'password' in self.fields:
            usuario_id = self.instance.pk if self.instance else '0'
            self.fields['password'].help_text = mark_safe(
                f'¿Necesitas cambiar la contraseña de este usuario? <a class="text-blue-600 underline hover:text-blue-800" href="/auth/usuarios/{usuario_id}/set-password/">Haz clic aquí para cambiarla</a>.'
            )
            self.fields['password'].label = "Contraseña"

class ProfesorCreationForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password1', 'password2', 'colegio']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['rol'] = forms.CharField(initial='profesor', widget=forms.HiddenInput())

        if user and user.rol == 'coordinador':
            self.fields['colegio'].queryset = Colegio.objects.filter(pk=user.colegio_id)
            self.fields['colegio'].initial = user.colegio
            self.fields['colegio'].widget = forms.HiddenInput()
        else:
            self.fields['colegio'].queryset = Colegio.objects.all()


class ProfesorChangeForm(UserChangeForm):
    password = None

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'rol', 'colegio']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['rol'].choices = [('profesor', 'Profesor')]
        self.fields['rol'].widget = forms.HiddenInput()

        if user and user.rol == 'coordinador':
            self.fields['colegio'].queryset = Colegio.objects.filter(pk=user.colegio_id)
            self.fields['colegio'].initial = user.colegio
            self.fields['colegio'].widget = forms.HiddenInput()

        # 👇 Agregar ayuda al campo de contraseña como link a restablecer
        if 'password' in self.fields:
            profesor_id = self.instance.pk if self.instance else '0'
            self.fields['password'].help_text = mark_safe(
                f'¿Olvidaste la contraseña de este usuario? <a class="text-blue-600 underline hover:text-blue-800" href="/auth/usuarios/{profesor_id}/password/">Establecer nueva contraseña</a>'
            )
            self.fields['password'].label = "Contraseña"
