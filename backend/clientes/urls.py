# registro_asistencia/backend/clientes/urls.py

from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    # Dueños
    path('duenos/',          views.dueno_list,   name='dueno_list'),
    path('duenos/crear/',    views.dueno_create, name='dueno_create'),
    path('duenos/<int:pk>/editar/',  views.dueno_edit,   name='dueno_edit'),
    path('duenos/<int:pk>/borrar/',  views.dueno_delete, name='dueno_delete'),

    # Colegios
    path('',                 views.colegio_list,   name='colegio_list'),
    path('crear/',           views.colegio_create, name='colegio_create'),
    path('<int:pk>/editar/', views.colegio_edit,   name='colegio_edit'),
    path('<int:pk>/borrar/', views.colegio_delete, name='colegio_delete'),

    # Reporte de Asistencia (opcional filtro por colegio)
    path('reporte/',                     views.reporte_asistencia, name='reporte_asistencia'),
    path('reporte/<int:colegio_id>/',    views.reporte_asistencia, name='reporte_asistencia_colegio'),
]
