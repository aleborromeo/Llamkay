from django.db import models


class Chat(models.Model):
    """Modelo para representar una conversación entre dos usuarios"""
    id_chat = models.AutoField(primary_key=True)
    usuario_1 = models.ForeignKey(
        'users.Usuario', 
        on_delete=models.CASCADE, 
        related_name='chats_iniciados',
        null=True, 
        blank=True
    )
    usuario_2 = models.ForeignKey(
        'users.Usuario', 
        on_delete=models.CASCADE, 
        related_name='chats_recibidos',
        null=True, 
        blank=True
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat'
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'
        constraints = [
            models.UniqueConstraint(
                fields=['usuario_1', 'usuario_2'], 
                name='unique_chat_pair'
            )
        ]
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Chat entre {self.usuario_1} y {self.usuario_2}"

    def obtener_otro_usuario(self, usuario_actual):
        """Retorna el otro usuario del chat"""
        return self.usuario_2 if self.usuario_1 == usuario_actual else self.usuario_1

    def obtener_ultimo_mensaje(self):
        """Retorna el último mensaje del chat"""
        return self.mensaje_set.filter(eliminado=False).order_by('-fecha_envio').first()


class Mensaje(models.Model):
    """Modelo para representar un mensaje dentro de un chat"""
    id_mensaje = models.AutoField(primary_key=True)
    id_chat = models.ForeignKey(
        Chat, 
        on_delete=models.CASCADE, 
        db_column='id_chat',
        related_name='mensajes'
    )
    remitente = models.ForeignKey(
        'users.Usuario', 
        on_delete=models.CASCADE,
        related_name='mensajes_enviados'
    )
    contenido = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    editado = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)
    leido = models.BooleanField(default=False)

    class Meta:
        db_table = 'mensaje'
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
        ordering = ['fecha_envio']

    def __str__(self):
        estado = "(eliminado)" if self.eliminado else "(editado)" if self.editado else ""
        return f"Mensaje de {self.remitente} {estado}"

    def marcar_como_leido(self):
        """Marca el mensaje como leído"""
        if not self.leido:
            self.leido = True
            self.save(update_fields=['leido'])

    def puede_editar(self, usuario):
        """Verifica si un usuario puede editar este mensaje"""
        return self.remitente == usuario and not self.eliminado

    def puede_eliminar(self, usuario):
        """Verifica si un usuario puede eliminar este mensaje"""
        return self.remitente == usuario and not self.eliminado