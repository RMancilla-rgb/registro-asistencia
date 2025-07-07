from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.db.models import ProtectedError

from .models import Usuario
from .forms import (
    UsuarioCreationForm, UsuarioChangeForm,
    ProfesorCreationForm, ProfesorChangeForm
)

# ————————————————————————————————————————————————————————
#  Permisos
# ————————————————————————————————————————————————————————

def is_administrador(user):
    return user.is_authenticated and user.rol == 'administrador'

def can_manage_profesores(user):
    return user.is_authenticated and user.rol in ['administrador', 'coordinador']

# ————————————————————————————————————————————————————————
#  CRUD Usuarios (solo ADMIN)
# ————————————————————————————————————————————————————————

@login_required
@user_passes_test(is_administrador)
def user_list(request):
    query = request.GET.get('q', '').strip()
    rol = request.GET.get('rol', '').strip()

    usuarios = Usuario.objects.exclude(pk=request.user.pk)

    if query:
        usuarios = usuarios.filter(username__icontains=query)

    if rol:
        usuarios = usuarios.filter(rol__iexact=rol)

    return render(request, 'usuarios/user_list.html', {'usuarios': usuarios})

@login_required
@user_passes_test(is_administrador)
def user_create(request):
    form = UsuarioCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Usuario creado correctamente.")
        return redirect('usuarios:user_list')
    return render(request, 'usuarios/user_form.html', {
        'form': form,
        'title': 'Crear Usuario'
    })

@login_required
@user_passes_test(is_administrador)
def user_edit(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    form = UsuarioChangeForm(request.POST or None, instance=usuario)
    if form.is_valid():
        form.save()
        messages.success(request, "Usuario actualizado correctamente.")
        return redirect('usuarios:user_list')
    return render(request, 'usuarios/user_form.html', {
        'form': form, 'title': 'Editar Usuario'
    })

@login_required
@user_passes_test(is_administrador)
def user_delete(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == 'POST':
        try:
            usuario.delete()
            messages.success(request, "Usuario eliminado correctamente.")
        except ProtectedError:
            messages.error(request, "No se puede eliminar este usuario porque está vinculado a registros importantes (como un cliente o dueño).")
        return redirect('usuarios:user_list')

    return render(request, 'usuarios/user_confirm_delete.html', {
        'object': usuario,
        'title': 'Borrar Usuario',
        'cancel_url': 'usuarios:user_list'
    })


# ————————————————————————————————————————————————————————
#  CAMBIAR CONTRASEÑA (ADMIN y COORD)
# ————————————————————————————————————————————————————————

@login_required
@user_passes_test(can_manage_profesores)
def user_set_password(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    # Solo coordinadores pueden editar contraseñas de profesores
    if request.user.rol == 'coordinador' and usuario.rol != 'profesor':
        messages.error(request, "Solo puedes cambiar la contraseña de profesores.")
        return redirect('usuarios:profesor_list')

    form = PasswordChangeForm(user=usuario, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        update_session_auth_hash(request, usuario)
        messages.success(request, f"Contraseña actualizada para {usuario.username}.")
        return redirect('usuarios:profesor_list' if request.user.rol == 'coordinador' else 'usuarios:user_list')

    return render(request, 'usuarios/set_password.html', {
        'form': form,
        'usuario': usuario,
    })

# ————————————————————————————————————————————————————————
#  CRUD Profesores (COORD/ADMIN)
# ————————————————————————————————————————————————————————

@login_required
@user_passes_test(can_manage_profesores)
def profesor_list(request):
    if request.user.rol == 'coordinador':
        colegio = getattr(request.user, 'colegio', None)
        profs = Usuario.objects.filter(rol='profesor', colegio=colegio)
    else:
        profs = Usuario.objects.filter(rol='profesor')

    return render(request, 'usuarios/profesor_list.html', {'profs': profs})

@login_required
@user_passes_test(can_manage_profesores)
def profesor_create(request):
    form = ProfesorCreationForm(request.POST or None, user=request.user)

    if request.method == 'POST' and form.is_valid():
        profesor = form.save(commit=False)
        profesor.rol = 'profesor'
        if request.user.rol == 'coordinador':
            profesor.colegio = request.user.colegio
        profesor.save()
        messages.success(request, "Profesor creado correctamente.")
        return redirect('usuarios:profesor_list')

    return render(request, 'usuarios/profesor_form.html', {
        'form': form,
        'title': 'Crear Profesor'
    })

@login_required
@user_passes_test(can_manage_profesores)
def profesor_edit(request, pk):
    prof = get_object_or_404(Usuario, pk=pk, rol='profesor')
    form = ProfesorChangeForm(request.POST or None, instance=prof, user=request.user)

    if form.is_valid():
        profesor = form.save(commit=False)

        # Si el usuario es coordinador, forzarle el colegio del coordinador
        if request.user.rol == 'coordinador':
            profesor.colegio = request.user.colegio

        profesor.save()
        messages.success(request, "Profesor actualizado correctamente.")
        return redirect('usuarios:profesor_list')

    return render(request, 'usuarios/profesor_form.html', {
        'form': form,
        'title': 'Editar Profesor'
    })

@login_required
@user_passes_test(can_manage_profesores)
def profesor_delete(request, pk):
    prof = get_object_or_404(Usuario, pk=pk, rol='profesor')
    if request.method == 'POST':
        prof.delete()
        messages.success(request, "Profesor eliminado correctamente.")
        return redirect('usuarios:profesor_list')
    return render(request, 'usuarios/profesor_confirm_delete.html', {
        'object': prof,
        'title': 'Borrar Profesor',
        'cancel_url': 'usuarios:profesor_list'
    })

# ————————————————————————————————————————————————————————
#  Login / Logout y Home
# ————————————————————————————————————————————————————————

class RoleBasedLoginView(LoginView):
    template_name = 'usuarios/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.rol == 'administrador':
            return reverse_lazy('usuarios:user_list')
        if user.rol == 'coordinador':
            return reverse_lazy('cursos:list')
        if user.rol == 'profesor':
            return reverse_lazy('talleres:index')
        if user.rol == 'cliente':
            return reverse_lazy('clientes:colegio_list')
        if user.rol == 'supervisor':
            return reverse_lazy('asistencia:supervision')
        return reverse_lazy('usuarios:login')

class LogoutGetView(LogoutView):
    http_method_names = ['get', 'post']
    next_page = 'usuarios:login'

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

@login_required
def home(request):
    rol = request.user.rol

    if rol == 'administrador':
        return redirect('usuarios:user_list')
    if rol == 'coordinador':
        return redirect('talleres:index')
    if rol == 'profesor':
        return redirect('talleres:index')
    if rol == 'cliente':
        return redirect('clientes:colegio_list')
    if rol == 'supervisor':
        return redirect('asistencia:supervision')

    return redirect('usuarios:login')
