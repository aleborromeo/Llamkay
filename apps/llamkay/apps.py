from django.apps import AppConfig


class LlamkayConfig(AppConfig):
    """Configuración del módulo llamkay (páginas estáticas)"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.llamkay'
    verbose_name = 'Llamkay General'