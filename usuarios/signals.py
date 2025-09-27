from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from usuarios.models import Usuario
from .models import Profile


@receiver(post_save, sender=User)
def crear_profile_usuario(sender, instance, created, **kwargs):
    if created:
        try:
            usuario = Usuario.objects.get(id_usuario=instance.id)
            Profile.objects.create(user=instance, usuario=usuario)
        except Usuario.DoesNotExist:
            pass