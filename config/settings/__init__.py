"""
Settings package initialization.

Por defecto, carga la configuración de desarrollo.
Para producción, establecer: DJANGO_SETTINGS_MODULE=config.settings.production
"""

import os

# Determinar qué configuración usar
ENVIRONMENT = os.environ.get('DJANGO_ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    from .production import *
else:
    from .development import *