from django.db import models
from django.contrib.auth.models import User

from usuarios.models import (
    Usuario,
    Profile,
    Habilidad,
    UsuarioHabilidad,
    Categoriatrabajo,
    UsuarioCategoria,
)

        
class Chat(models.Model):
    id_chat = models.AutoField(primary_key=True)
    usuario_1 = models.ForeignKey(Usuario, models.DO_NOTHING, related_name='chats_iniciados',null=True, blank=True)
    usuario_2 = models.ForeignKey(Usuario, models.DO_NOTHING, related_name='chats_recibidos',null=True, blank=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'chat'
        constraints = [
            models.UniqueConstraint(fields=['usuario_1', 'usuario_2'], name='unique_chat_pair')
        ]


class Mensaje(models.Model):
    id_mensaje = models.AutoField(primary_key=True)
    id_chat = models.ForeignKey(Chat, models.DO_NOTHING, db_column='id_chat')
    remitente = models.ForeignKey(Usuario, models.DO_NOTHING)
    contenido = models.TextField(blank=True, null=True)
    fecha_envio = models.DateTimeField(blank=True, null=True)
    editado = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)
    leido = models.BooleanField(default=False)

    class Meta:
        db_table = 'mensaje'
