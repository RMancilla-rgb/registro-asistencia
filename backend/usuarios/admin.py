from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class CustomUserAdmin(UserAdmin):
    # Para la vista de edición
    fieldsets = UserAdmin.fieldsets + (
        ('Información de Rol', {'fields': ('rol',)}),
    )
    # Para la vista de creación
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Información de Rol', {
            'classes': ('wide',),
            'fields': ('rol',),
        }),
    )
    list_display = UserAdmin.list_display + ('rol',)
