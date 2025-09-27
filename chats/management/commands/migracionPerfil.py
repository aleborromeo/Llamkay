from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from usuarios.models import Usuario

class Command(BaseCommand):
    help = 'Crea perfiles extendidos para todos los usuarios que no lo tengan'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            perfil, creado = Usuario.objects.get_or_create(user=user)
            if creado:
                self.stdout.write(f"Perfil creado para usuario: {user.username}")
            else:
                self.stdout.write(f"Perfil ya existe para usuario: {user.username}")
        self.stdout.write(self.style.SUCCESS('Migración de perfiles completada.'))
