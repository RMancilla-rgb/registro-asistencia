# registro_asistencia/backend/clientes/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import ProtectedError
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Dueno, Colegio
from .forms import DuenoForm, ColegioForm
from asistencia.models import Asistencia


# — Permisos personalizados —

def is_admin(user):
    return user.is_authenticated and user.rol == 'administrador'

def can_view_colegios(user):
    # Administrador y Cliente pueden ver la lista de colegios
    return user.is_authenticated and user.rol in ('administrador', 'cliente')

def can_view_reportes(user):
    # Admin, Coordinador y Cliente pueden ver informes
    return user.is_authenticated and user.rol in ('administrador', 'coordinador', 'cliente')


# Parámetros comunes a login_required
LOGIN_KWARGS = {
    'login_url': reverse_lazy('usuarios:login'),
    'redirect_field_name': None,
}


# — CRUD Dueños (sólo admin) —

@login_required(**LOGIN_KWARGS)
@user_passes_test(is_admin, login_url=reverse_lazy('usuarios:home'), redirect_field_name=None)
def dueno_list(request):
    duenos = Dueno.objects.all()
    return render(request, 'clientes/dueno_list.html', {'duenos': duenos})

@login_required(**LOGIN_KWARGS)
@user_passes_test(is_admin, login_url=reverse_lazy('usuarios:home'), redirect_field_name=None)
def dueno_create(request):
    form = DuenoForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Cliente creada correctamente.")
        return redirect('clientes:dueno_list')
    return render(request, 'clientes/form.html', {
        'form': form,
        'title': 'Crear Cliente',
    })

@login_required(**LOGIN_KWARGS)
@user_passes_test(is_admin, login_url=reverse_lazy('usuarios:home'), redirect_field_name=None)
def dueno_edit(request, pk):
    dueno = get_object_or_404(Dueno, pk=pk)
    form = DuenoForm(request.POST or None, instance=dueno)
    if form.is_valid():
        form.save()
        messages.success(request, "Cliente actualizada correctamente.")
        return redirect('clientes:dueno_list')
    return render(request, 'clientes/form.html', {
        'form': form,
        'title': 'Editar Cliente',
    })

@login_required(**LOGIN_KWARGS)
@user_passes_test(is_admin, login_url=reverse_lazy('usuarios:home'), redirect_field_name=None)
def dueno_delete(request, pk):
    dueno = get_object_or_404(Dueno, pk=pk)
    if request.method == 'POST':
        try:
            dueno.delete()
            messages.success(request, "Cliente eliminada correctamente.")
        except ProtectedError:
            messages.error(
                request,
                "No se puede borrar esta Cliente porque tiene colegios o cursos asociados."
            )
        return redirect('clientes:dueno_list')
    return render(request, 'clientes/confirm_delete.html', {
        'object': dueno,
        'title': 'Borrar Cliente',
        'cancel_url': 'clientes:dueno_list',
    })


# — CRUD Colegios — 

# Listar: admin + cliente
@login_required(**LOGIN_KWARGS)
@user_passes_test(can_view_colegios, login_url=reverse_lazy('usuarios:home'), redirect_field_name=None)
def colegio_list(request):
    query = request.GET.get('q', '').strip()
    dueno_id = request.GET.get('dueno', '').strip()

    if request.user.rol == 'cliente':
        try:
            dueno = request.user.dueno
            colegios = Colegio.objects.filter(dueno=dueno)
            duenos = []  # clientes no ven selector de dueños
        except Dueno.DoesNotExist:
            colegios = Colegio.objects.none()
            duenos = []
    else:
        colegios = Colegio.objects.select_related('dueno').all()

        # Cargar lista de dueños para el selector
        duenos = Dueno.objects.select_related('user').all()

        if dueno_id:
            colegios = colegios.filter(dueno_id=dueno_id)

    if query:
        colegios = colegios.filter(nombre__icontains=query)

    return render(request, 'clientes/colegio_list.html', {
        'colegios': colegios,
        'duenos': duenos,
    })



# Crear/editar/borrar: sólo admin
@login_required(**LOGIN_KWARGS)
@user_passes_test(is_admin, login_url=reverse_lazy('usuarios:home'), redirect_field_name=None)
def colegio_create(request):
    form = ColegioForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Colegio creado correctamente.")
        return redirect('clientes:colegio_list')
    return render(request, 'clientes/form.html', {
        'form': form,
        'title': 'Crear Colegio',
    })

@login_required(**LOGIN_KWARGS)
@user_passes_test(is_admin, login_url=reverse_lazy('usuarios:home'), redirect_field_name=None)
def colegio_edit(request, pk):
    colegio = get_object_or_404(Colegio, pk=pk)
    form = ColegioForm(request.POST or None, instance=colegio)
    if form.is_valid():
        form.save()
        messages.success(request, "Colegio actualizado correctamente.")
        return redirect('clientes:colegio_list')
    return render(request, 'clientes/form.html', {
        'form': form,
        'title': 'Editar Colegio',
    })

@login_required(**LOGIN_KWARGS)
@user_passes_test(is_admin, login_url=reverse_lazy('usuarios:home'), redirect_field_name=None)
def colegio_delete(request, pk):
    colegio = get_object_or_404(Colegio, pk=pk)
    if request.method == 'POST':
        try:
            colegio.delete()
            messages.success(request, "Colegio eliminado correctamente.")
        except ProtectedError:
            messages.error(
                request,
                "No se puede borrar este colegio porque tiene cursos o alumnos asociados."
            )
        return redirect('clientes:colegio_list')
    return render(request, 'clientes/confirm_delete.html', {
        'object': colegio,
        'title': 'Borrar Colegio',
        'cancel_url': 'clientes:colegio_list',
    })


# — Informe de asistencia — 

@login_required(**LOGIN_KWARGS)
@user_passes_test(can_view_reportes, login_url=reverse_lazy('usuarios:home'), redirect_field_name=None)
def reporte_asistencia(request, colegio_id=None):
    qs = Asistencia.objects.select_related('taller__curso__colegio', 'alumno')
    if colegio_id:
        qs = qs.filter(taller__curso__colegio__id=colegio_id)
    elif request.user.rol == 'cliente':
        try:
            dueno = request.user.dueno
            qs = qs.filter(taller__curso__colegio__dueno=dueno)
        except:
            qs = qs.none()
    asistencias = qs.order_by('-fecha')
    return render(request, 'clientes/reporte_asistencia.html', {
        'asistencias': asistencias,
        'colegio_id': colegio_id,
    })

