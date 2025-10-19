from django.apps import AppConfig

class UsuariosConfig(AppConfig):
    name = 'apps.users'

    def ready(self):
        import apps.users.signals  # 👈 esto es lo que carga las señales
