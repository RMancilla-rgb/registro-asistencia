from django.contrib import admin
from .models import Asistencia

@admin.register(Asistencia)
class AsistenciaAdmin(admin.ModelAdmin):
    list_display   = ('fecha', 'taller', 'alumno', 'estado')
    list_filter    = ('fecha', 'estado', 'taller__curso__ciclo')
    search_fields  = ('alumno__nombre',)
