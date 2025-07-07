from django.urls import path
from . import views

app_name = 'cursos'

urlpatterns = [
    # Cursos
    path('', views.curso_list, name='list'),
    path('crear/', views.curso_create, name='create'),
    path('<int:pk>/editar/', views.curso_edit,   name='edit'),
    path('<int:pk>/borrar/', views.curso_delete, name='delete'),
    # Alumnos
    path('alumnos/',                views.alumno_list,   name='alumno_list'),
    path('alumnos/crear/',          views.alumno_create, name='alumno_create'),
    path('alumnos/<int:pk>/editar/',views.alumno_edit,   name='alumno_edit'),
    path('alumnos/<int:pk>/borrar/',views.alumno_delete, name='alumno_delete'),
]

