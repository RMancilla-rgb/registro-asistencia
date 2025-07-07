from django.contrib import admin
from .models import Dueno, Colegio

@admin.register(Dueno)
class DuenoAdmin(admin.ModelAdmin):
    list_display  = ('nombre',)
    search_fields = ('nombre',)

@admin.register(Colegio)
class ColegioAdmin(admin.ModelAdmin):
    list_display    = ('nombre', 'dueno', 'coordinador')
    list_filter     = ('dueno', 'coordinador')
    search_fields   = ('nombre',)
