# backend/coordinacion/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test, login_required

def is_coordinador(user):
    return user.is_authenticated and user.rol == 'coordinador'

@login_required
@user_passes_test(is_coordinador)
def index(request):
    # aquí más lógica: lista de talleres, alumnos, etc.
    return render(request, 'coordinacion/index.html')
