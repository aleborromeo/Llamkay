"""
URL configuration for Llamkay project.
"""
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# URLs que NO necesitan i18n (admin, APIs, AJAX)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

# URLs con soporte i18n
urlpatterns += i18n_patterns(
    path('', include('apps.llamkay.urls')),
    path('users/', include('apps.users.urls')),
    path('jobs/', include('apps.jobs.urls')),
    path('empleadores/', include('apps.empleadores.urls')),
    path('chats/', include('apps.chats.urls')),
    path('soporte/', include('apps.soporte.urls')),
    path('pagos/', include('apps.monetizacion.urls')),
)

# Servir archivos estáticos en desarrollo
if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Personalizar admin
admin.site.site_header = "Llamkay Admin"
admin.site.site_title = "Llamkay Admin Portal"
admin.site.index_title = "Bienvenido al Panel de Administración de Llamkay"