"""
URL configuration for Llamkay project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Apps principales
    path('', include('apps.llamkay.urls')),  # Home/landing
    path('users/', include('apps.users.urls')),
    path('jobs/', include('apps.jobs.urls')),
    path('chats/', include('apps.chats.urls')),
    path('soporte/', include('apps.soporte.urls')),
]

# Servir archivos estáticos en desarrollo
if settings.DEBUG:
    # Servir archivos estáticos desde STATICFILES_DIRS
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
    
    # Servir archivos media
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Personalizar admin
admin.site.site_header = "Llamkay Admin"
admin.site.site_title = "Llamkay Admin Portal"
admin.site.index_title = "Bienvenido al Panel de Administración de Llamkay"