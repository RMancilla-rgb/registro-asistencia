from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # alias no-namespaced para reverse('login')
    path('login/',
         RedirectView.as_view(pattern_name='usuarios:login', permanent=False),
         name='login'),

    # opcional: redirigir “/” al login
    path('',
         RedirectView.as_view(pattern_name='login', permanent=False)),

    # auth
    path('auth/', include('usuarios.urls')),

    # nuestros módulos
     path('admin/', admin.site.urls),
    path('coordinacion/',  include(('coordinacion.urls',  'coordinacion'),  namespace='coordinacion')),
    path('talleres/',      include(('talleres.urls',      'talleres'),      namespace='talleres')),
    path('asistencia/',    include(('asistencia.urls',    'asistencia'),    namespace='asistencia')),
    path('clientes/', include(('clientes.urls', 'clientes'), namespace='clientes')),
    path('cursos/',        include(('cursos.urls',        'cursos'),        namespace='cursos' )),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
