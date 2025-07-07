from django.contrib import admin
from .models import Curso, Alumno

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('ciclo', 'grado')
    list_filter  = ('ciclo',)

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'rut', 'curso')
    search_fields = ('nombre', 'rut')
    list_filter   = ('curso__ciclo', 'curso__grado')
