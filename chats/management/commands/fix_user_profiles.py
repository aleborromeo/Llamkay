from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from usuarios.models import Usuario


class Command(BaseCommand):
    help = 'Verifica y crea perfiles faltantes para usuarios'

    def handle(self, *args, **options):
        users_without_profile = []
        users_with_profile = []
        
        for user in User.objects.all():
            try:
                # Verificar si el usuario tiene perfil
                profile = user.perfil
                users_with_profile.append(user.username)
                self.stdout.write(f"✓ Usuario {user.username} tiene perfil: {profile.nombres} {profile.apellidos}")
            except Usuario.DoesNotExist:
                users_without_profile.append(user.username)
                self.stdout.write(self.style.WARNING(f"⚠ Usuario {user.username} NO tiene perfil"))
                
                # Crear perfil básico
                usuario = Usuario.objects.create(
                    user=user,
                    username=user.username,
                    nombres=user.first_name or user.username,
                    apellidos=user.last_name or "",
                    email=user.email,
                    tipo_usuario='buscar-trabajo',
                    habilitado=True
                )
                self.stdout.write(self.style.SUCCESS(f"✓ Perfil creado para {user.username}"))
        
        self.stdout.write(f"\nResumen:")
        self.stdout.write(f"Usuarios con perfil: {len(users_with_profile)}")
        self.stdout.write(f"Usuarios sin perfil (corregidos): {len(users_without_profile)}")
