"""
Modelos de Chats - Simplificado
"""
from django.db import models


class Conversacion(models.Model):
    id_conversacion = models.AutoField(primary_key=True)
    id_usuario_1 = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        related_name='conversaciones_iniciadas'
    )
    id_usuario_2 = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        related_name='conversaciones_recibidas'
    )
    
    # Contexto (opcional)
    id_oferta_usuario = models.ForeignKey(
        'jobs.OfertaUsuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    id_oferta_empresa = models.ForeignKey(
        'jobs.OfertaEmpresa',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Estado
    activa = models.BooleanField(default=True)
    bloqueada = models.BooleanField(default=False)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ultimo_mensaje_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'conversacion'
        unique_together = [['id_usuario_1', 'id_usuario_2']]

    def __str__(self):
        return f"Conversación {self.id_conversacion}"


class Mensaje(models.Model):
    TIPO_CHOICES = [
        ('texto', 'Texto'),
        ('imagen', 'Imagen'),
        ('archivo', 'Archivo'),
    ]

    id_mensaje = models.AutoField(primary_key=True)
    id_conversacion = models.ForeignKey(
        Conversacion,
        on_delete=models.CASCADE,
        related_name='mensajes'
    )
    id_remitente = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        related_name='mensajes_enviados'
    )
    
    # Contenido
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='texto')
    contenido = models.TextField(null=True, blank=True)
    archivo = models.CharField(max_length=500, null=True, blank=True)
    
    # Estado
    leido = models.BooleanField(default=False)
    fecha_leido = models.DateTimeField(null=True, blank=True)
    eliminado = models.BooleanField(default=False)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'mensaje'
        ordering = ['created_at']

    def __str__(self):
        return f"Mensaje {self.id_mensaje}"