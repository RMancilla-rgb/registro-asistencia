# backend/cursos/urls.py

from django.urls import path
from . import views

app_name = 'cursos'

urlpatterns = [
    # CRUD de cursos
    path('',               views.curso_list,   name='list'),
    path('create/',        views.curso_create, name='create'),
    path('<int:pk>/edit/', views.curso_edit,   name='edit'),
    path('<int:pk>/delete/', views.curso_delete, name='delete'),

    # CRUD de alumnos
    path('alumnos/',               views.alumno_list,   name='alumno_list'),
    path('alumnos/create/',        views.alumno_create, name='alumno_create'),
    path('alumnos/<int:pk>/edit/', views.alumno_edit,   name='alumno_edit'),
    path('alumnos/<int:pk>/delete/', views.alumno_delete, name='alumno_delete'),
]
