from django.urls import path
from . import views
from .views import supervisar_colegios

app_name = 'asistencia'

urlpatterns = [
    # Vista principal para profesores (ver talleres y pasar lista)
    path('', views.index, name='index'),

    # Formulario para marcar asistencia a un taller
    path('marcar/<int:taller_id>/', views.marcar_asistencia, name='marcar'),

    # Vista de supervisión (solo supervisores)
    path('supervision/', views.supervisar_asistencia, name='supervision'),

    # Informe general (para admin y coordinador)
    path('reportes/', views.reporte_asistencia, name='reportes'),

    # Selección de taller para reporte detallado
    path('reporte/seleccionar/', views.seleccionar_reporte, name='seleccionar_reporte'),

    # Reporte detallado de un taller específico
    path('reporte/<int:taller_id>/', views.reporte_taller, name='reporte_taller'),

    # Descargar Excel de un taller
    path('reporte/<int:taller_id>/excel/', views.descargar_reporte_excel, name='descargar_excel'),

    # Subida de Excel de asistencia
    path('subir_excel/', views.subir_asistencia_excel, name='subir_asistencia_excel'),
   
    path('supervisar/colegios/', views.supervisar_colegios, name='supervisar_colegios'),

    path('supervision/', views.supervisar_asistencia, name='supervisar_asistencia'),
    
    path('supervisar/colegios/', views.supervisar_colegios, name='supervisar_colegios'),

    path('supervisar/colegios/mes/', views.supervisar_colegios_mes, name='supervisar_colegios_mes'),

    
]

