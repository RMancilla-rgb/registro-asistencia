# backend/coordinacion/urls.py
from django.urls import path
from .views import index

app_name = 'coordinacion'

urlpatterns = [
    path('', index, name='index'),
]
