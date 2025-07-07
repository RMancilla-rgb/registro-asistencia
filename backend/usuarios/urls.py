# backend/usuarios/urls.py

from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.home, name='home'),

    # login / logout
    path('login/',  views.RoleBasedLoginView.as_view(), name='login'),
    path('logout/', views.LogoutGetView.as_view(),      name='logout'),

    # CRUD Usuarios
    path('usuarios/',         views.user_list,   name='user_list'),
    path('usuarios/crear/',   views.user_create, name='user_create'),
    path('usuarios/<int:pk>/editar/', views.user_edit,   name='user_edit'),
    path('usuarios/<int:pk>/borrar/', views.user_delete, name='user_delete'),

    # CRUD Profesores
    path('profesores/',           views.profesor_list,   name='profesor_list'),
    path('profesores/crear/',     views.profesor_create, name='profesor_create'),
    path('profesores/<int:pk>/editar/', views.profesor_edit,   name='profesor_edit'),
    path('profesores/<int:pk>/borrar/', views.profesor_delete, name='profesor_delete'),


    path('usuarios/<int:pk>/password/', views.user_set_password, name='user_set_password'),

]
