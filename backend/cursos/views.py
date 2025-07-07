# registro_asistencia/backend/cursos/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import ProtectedError, Q
from django.contrib import messages

from .models import Curso, Alumno
from .forms import CursoForm, AlumnoForm
from clientes.models import Colegio

# Permiso: coordinador y administrador
def can_manage_cursos(user):
    return user.is_authenticated and user.rol in ('coordinador', 'administrador')

# --- CRUD de Cursos ---

@login_required
@user_passes_test(can_manage_cursos)
def curso_list(request):
    query = request.GET.get('q', '').strip()
    colegio_id = request.GET.get('colegio', '').strip()

    if request.user.rol == 'coordinador':
        colegio = getattr(request.user, 'colegio', None)
        if colegio:
            cursos = Curso.objects.filter(colegio=colegio)
            colegios = Colegio.objects.filter(id=colegio.id)
        else:
            cursos = Curso.objects.none()
            colegios = Colegio.objects.none()
    else:
        cursos = Curso.objects.select_related('colegio').all()
        colegios = Colegio.objects.all()

    if query:
        cursos = cursos.filter(
            Q(ciclo__icontains=query) |
            Q(grado__icontains=query) |
            Q(colegio__nombre__icontains=query)
        )

    if colegio_id:
        cursos = cursos.filter(colegio_id=colegio_id)

    return render(request, 'cursos/list.html', {
        'cursos': cursos,
        'colegios': colegios,
    })

@login_required
@user_passes_test(can_manage_cursos)
def curso_create(request):
    form = CursoForm(request.POST or None, user=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, "Curso creado correctamente.")
        return redirect('cursos:list')
    return render(request, 'cursos/form.html', {'form': form, 'title': 'Crear Curso'})

@login_required
@user_passes_test(can_manage_cursos)
def curso_edit(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    form = CursoForm(request.POST or None, instance=curso)
    if form.is_valid():
        form.save()
        messages.success(request, "Curso actualizado correctamente.")
        return redirect('cursos:list')
    return render(request, 'cursos/form.html', {'form': form, 'title': 'Editar Curso'})

@login_required
@user_passes_test(can_manage_cursos)
def curso_delete(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        try:
            curso.delete()
            messages.success(request, f"Curso «{curso.get_ciclo_display()} {curso.grado}°» eliminado correctamente.")
        except ProtectedError:
            messages.error(
                request,
                "No se puede borrar el curso porque tiene alumnos asignados. "
                "Primero elimina o reasigna a esos alumnos."
            )
        return redirect('cursos:list')
    return render(request, 'cursos/confirm_delete.html', {'curso': curso})

# --- CRUD de Alumnos ---

@login_required
@user_passes_test(can_manage_cursos)
def alumno_list(request):
    query = request.GET.get('q', '').strip()
    colegio_id = request.GET.get('colegio', '').strip()
    curso_id = request.GET.get('curso', '').strip()

    if request.user.rol == 'coordinador':
        colegio = getattr(request.user, 'colegio', None)
        if colegio:
            alumnos = Alumno.objects.filter(curso__colegio=colegio)
            colegios = Colegio.objects.filter(id=colegio.id)
            cursos = Curso.objects.filter(colegio=colegio)
        else:
            alumnos = Alumno.objects.none()
            colegios = Colegio.objects.none()
            cursos = Curso.objects.none()
    else:
        alumnos = Alumno.objects.select_related('curso__colegio').all()
        colegios = Colegio.objects.all()
        cursos = Curso.objects.all()

    if colegio_id:
        alumnos = alumnos.filter(curso__colegio_id=colegio_id)
        cursos = cursos.filter(colegio_id=colegio_id)

    if curso_id:
        alumnos = alumnos.filter(curso_id=curso_id)

    if query:
        alumnos = alumnos.filter(nombre__icontains=query)

    return render(request, 'cursos/alumno_list.html', {
        'alumnos': alumnos,
        'colegios': colegios,
        'cursos': cursos,
    })

@login_required
@user_passes_test(can_manage_cursos)
def alumno_create(request):
    form = AlumnoForm(request.POST or None, user=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, "Alumno creado correctamente.")
        return redirect('cursos:alumno_list')

    return render(request, 'cursos/alumno_form.html', {
        'form': form,
        'title': 'Crear Alumno',
    })

@login_required
@user_passes_test(can_manage_cursos)
def alumno_edit(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    form = AlumnoForm(request.POST or None, instance=alumno, user=request.user)

    if form.is_valid():
        form.save()
        messages.success(request, "Alumno actualizado correctamente.")
        return redirect('cursos:alumno_list')

    return render(request, 'cursos/alumno_form.html', {'form': form, 'title': 'Editar Alumno'})

@login_required
@user_passes_test(can_manage_cursos)
def alumno_delete(request, pk):
    alumno = get_object_or_404(Alumno, pk=pk)
    if request.method == 'POST':
        alumno.delete()
        messages.success(request, "Alumno eliminado correctamente.")
        return redirect('cursos:alumno_list')
    return render(request, 'cursos/alumno_confirm_delete.html', {'alumno': alumno})
