from django.urls import path
from . import views

app_name = 'talleres'

urlpatterns = [
    path('', views.index, name='index'),
    path('crear/', views.taller_create, name='create'),  # 👈 este es el nombre esperado
    path('<int:pk>/editar/', views.taller_edit, name='edit'),
    path('<int:pk>/borrar/', views.taller_delete, name='delete'),
    path('alumnos-por-curso/', views.alumnos_por_curso, name='alumnos_por_curso'),
    path('talleres/', views.talleres_list, name='talleres_list'),
]
