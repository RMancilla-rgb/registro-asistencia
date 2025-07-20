from django.contrib import admin
from .models import Taller

@admin.register(Taller)
class TallerAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'colegio', 'curso', 'profesor')
    list_filter  = ('colegio', 'curso__ciclo', 'curso__grado', 'profesor')
    filter_horizontal = ('alumnos',)
    search_fields = ('nombre',)