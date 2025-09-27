from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Usuario, Profile

@receiver(post_save, sender=User)
def crear_usuario(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'usuario'):
        Usuario.objects.create(user=instance, nombres=instance.first_name, apellidos=instance.last_name)

@receiver(post_save, sender=Usuario)
def crear_perfil(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
