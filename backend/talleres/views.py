# talleres/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from cursos.models import Curso, Alumno
from .models import Taller
from .forms import TallerForm
from django.contrib import messages

from django.http import JsonResponse

# --- Permisos ---
def can_view_talleres(user):
    return user.is_authenticated and user.rol in ('profesor', 'coordinador', 'administrador')

def can_manage_talleres(user):
    return user.is_authenticated and user.rol in ('coordinador', 'administrador')

# --- Listado: cualquier rol permitido ---
@login_required
@user_passes_test(can_view_talleres)
def index(request):
    query = request.GET.get('q')
    curso_id = request.GET.get('curso')

    if request.user.rol == 'profesor':
        talleres = Taller.objects.filter(profesor=request.user)
        cursos = Curso.objects.filter(talleres__profesor=request.user).distinct()
    elif request.user.rol == 'coordinador':
        colegio = getattr(request.user, 'colegio', None)
        talleres = Taller.objects.filter(curso__colegio=colegio)
        cursos = Curso.objects.filter(colegio=colegio)
    else:
        talleres = Taller.objects.select_related('curso').all()
        cursos = Curso.objects.all()

    if query:
        talleres = talleres.filter(nombre__icontains=query)


    if curso_id and curso_id != 'todos':
        talleres = talleres.filter(curso__id=curso_id)

    return render(request, 'talleres/list.html', {
        'talleres': talleres,
        'cursos': cursos,
        'curso_seleccionado': curso_id,
        'busqueda': query,
    })

# --- Crear ---
@login_required
@user_passes_test(can_manage_talleres)
def taller_create(request):
    form = TallerForm(request.POST or None, user=request.user)

    curso_id = request.GET.get('curso') or request.POST.get('curso')
    curso_obj = Curso.objects.filter(pk=curso_id).first() if curso_id else None

    # Fijar queryset de alumnos
    if curso_obj:
        form.fields['alumnos'].queryset = curso_obj.alumnos.all().order_by('nombre')
    else:
        form.fields['alumnos'].queryset = Alumno.objects.none()

    # Obtener los cursos según el colegio del usuario
    if request.user.rol == 'coordinador':
        cursos_queryset = Curso.objects.filter(colegio=request.user.colegio)
    else:
        cursos_queryset = Curso.objects.all()

    if request.method == 'POST' and form.is_valid():
        taller = form.save(commit=False)
        taller.curso = curso_obj
        taller.save()
        form.save_m2m()
        messages.success(request, "Taller creado correctamente.")
        return redirect('talleres:index')

    return render(request, 'talleres/form.html', {
        'form': form,
        'title': 'Crear Taller',
        'curso_obj': curso_obj,
        'cursos': cursos_queryset,
    })


# --- Editar ---
@login_required
@user_passes_test(can_manage_talleres)
def taller_edit(request, pk):
    taller = get_object_or_404(Taller, pk=pk)
    curso_id = request.GET.get('curso')
    curso_obj = Curso.objects.filter(pk=curso_id).first() if curso_id else taller.curso

    form = TallerForm(request.POST or None, instance=taller, user=request.user)

    if curso_obj:
        form.fields['alumnos'].queryset = curso_obj.alumnos.all().order_by('nombre')
    else:
        form.fields['alumnos'].queryset = Alumno.objects.none()

    alumnos_sel = request.POST.getlist('alumnos') if request.method == 'POST' else [str(a.pk) for a in taller.alumnos.all()]

    if request.method == 'POST' and form.is_valid():
        taller = form.save(commit=False)
        taller.curso = curso_obj
        taller.save()
        form.save_m2m()
        messages.success(request, "Taller actualizado correctamente.")
        return redirect('talleres:index')

    return render(request, 'talleres/taller_form.html', {
        'form': form,
        'title': 'Editar Taller',
        'curso_obj': curso_obj,
        'cursos': Curso.objects.select_related('colegio__dueno').all(),
        'alumnos_sel': alumnos_sel,
    })

# --- Borrar ---
@login_required
@user_passes_test(can_manage_talleres)
def taller_delete(request, pk):
    taller = get_object_or_404(Taller, pk=pk)
    if request.method == 'POST':
        taller.delete()
        return redirect('talleres:index')
    return render(request, 'talleres/confirm_delete.html', {'taller': taller})

@login_required
def alumnos_por_curso(request):
    curso_id = request.GET.get('curso_id')
    alumnos = Alumno.objects.filter(curso_id=curso_id).order_by('nombre')
    data = [{'id': a.id, 'nombre': a.nombre} for a in alumnos]
    return JsonResponse(data, safe=False)

def talleres_list(request):
    cursos = Curso.objects.all()
    query = request.GET.get('q')
    curso_id = request.GET.get('curso')

    talleres = Taller.objects.all()

    if query:
        talleres = talleres.filter(curso__nombre__icontains=query)

    if curso_id and curso_id != 'todos':
        talleres = talleres.filter(curso__id=curso_id)

    context = {
        'talleres': talleres,
        'cursos': cursos,
        'curso_seleccionado': curso_id,
        'busqueda': query,
    }
    return render(request, 'talleres/list.html', context)


def crear_taller(request):
    if request.method == 'POST':
        form = TallerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('talleres:index')
    else:
        form = TallerForm()
    return render(request, 'talleres/taller_form.html', {'form': form})