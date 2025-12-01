"""
Configuración del módulo de Soporte
"""
from django.apps import AppConfig


class SoporteConfig(AppConfig):
    """Configuración del módulo de Soporte"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.soporte'
    verbose_name = 'Soporte y Moderación'
    
    def ready(self):
        """
        Importar signals cuando la app esté lista
        """
        pass