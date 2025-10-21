from django.db import models


class Conversacion(models.Model):
    id_conversacion = models.AutoField(primary_key=True)
    id_usuario_1 = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        related_name='conversaciones_iniciadas',
        db_column='id_usuario_1'
    )
    id_usuario_2 = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        related_name='conversaciones_recibidas',
        db_column='id_usuario_2'
    )
    
    # Contexto
    id_oferta_usuario = models.ForeignKey(
        'jobs.OfertaUsuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_oferta_usuario'
    )
    id_oferta_empresa = models.ForeignKey(
        'jobs.OfertaEmpresa',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_oferta_empresa'
    )
    id_contrato = models.ForeignKey(
        'jobs.Contrato',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_contrato'
    )
    
    # Estado
    activa = models.BooleanField(default=True)
    bloqueada = models.BooleanField(default=False)
    id_bloqueada_por = models.ForeignKey(
        'users.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conversaciones_bloqueadas',
        db_column='id_bloqueada_por'
    )
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ultimo_mensaje_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'conversacion'
        unique_together = [['id_usuario_1', 'id_usuario_2']]
        indexes = [
            models.Index(fields=['id_usuario_1', 'activa']),
            models.Index(fields=['id_usuario_2', 'activa']),
            models.Index(fields=['-ultimo_mensaje_at'])
        ]

    def __str__(self):
        return f"Conversación entre {self.id_usuario_1} y {self.id_usuario_2}"

    def obtener_otro_usuario(self, usuario_actual):
        return self.id_usuario_2 if self.id_usuario_1 == usuario_actual else self.id_usuario_1


class Mensaje(models.Model):
    TIPO_MENSAJE_CHOICES = [
        ('texto', 'Texto'),
        ('imagen', 'Imagen'),
        ('archivo', 'Archivo'),
        ('ubicacion', 'Ubicación'),
        ('sistema', 'Sistema'),
    ]

    id_mensaje = models.AutoField(primary_key=True)
    id_conversacion = models.ForeignKey(
        'Conversacion',
        on_delete=models.CASCADE,
        related_name='mensajes',
        db_column='id_conversacion'
    )
    id_remitente = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        related_name='mensajes_enviados',
        db_column='id_remitente'
    )
    
    # Contenido
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_MENSAJE_CHOICES,
        default='texto'
    )
    contenido = models.TextField(null=True, blank=True)
    archivo = models.CharField(max_length=500, null=True, blank=True)
    
    # Estado
    leido = models.BooleanField(default=False)
    fecha_leido = models.DateTimeField(null=True, blank=True)
    editado = models.BooleanField(default=False)
    eliminado = models.BooleanField(default=False)
    
    # Auditoría
    fecha_envio = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mensaje'
        ordering = ['fecha_envio']
        indexes = [
            models.Index(fields=['id_conversacion', '-fecha_envio']),
            models.Index(fields=['id_remitente'])
        ]

    def __str__(self):
        estado = "(eliminado)" if self.eliminado else "(editado)" if self.editado else ""
        return f"Mensaje de {self.id_remitente} {estado}"

    def marcar_como_leido(self):
        if not self.leido:
            self.leido = True
            self.save(update_fields=['leido', 'fecha_leido'])