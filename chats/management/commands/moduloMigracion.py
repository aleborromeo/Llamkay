#migrar para poder usar auth_user de django y facilitar la autenticación
#python manage.py moduloMigracion

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from usuarios.models import Usuario  # tu modelo antiguo

class Command(BaseCommand): #migrar Usuarios
    help = 'Migra los usuarios desde la tabla antigua a auth_user'

    def handle(self, *args, **kwargs):
        usuarios = Usuario.objects.all()
        for u in usuarios:
            username = f'user{u.id_usuario}'
            if not User.objects.filter(username=username).exists():
                User.objects.create(
                    username=username,
                    first_name=u.nombres,
                    last_name=u.apellidos,
                    email=u.email,
                    password=make_password(u.clave),  # encripta la contraseña
                    is_active=True
                )
                self.stdout.write(self.style.SUCCESS(f'✅ Migrado: {username}'))
            else:
                self.stdout.write(self.style.WARNING(f'⚠️ Ya existe: {username}'))