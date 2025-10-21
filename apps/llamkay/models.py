from django.db import models


# ==================== DENUNCIAS Y DISPUTAS ====================
class Denuncia(models.Model):
    MOTIVO_DENUNCIA_CHOICES = [
        ('fraude', 'Fraude'),
        ('acoso', 'Acoso'),
        ('spam', 'Spam'),
        ('contenido_inapropiado', 'Contenido Inapropiado'),
        ('incumplimiento', 'Incumplimiento'),
        ('otro', 'Otro'),
    ]

    ESTADO_DENUNCIA_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En Revisión'),
        ('resuelta', 'Resuelta'),
        ('cerrada', 'Cerrada'),
        ('rechazada', 'Rechazada'),
    ]

    id_denuncia = models.AutoField(primary_key=True)
    id_reportante = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        related_name='denuncias_realizadas',
        db_column='id_reportante'
    )
    id_denunciado = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        related_name='denuncias_recibidas',
        db_column='id_denunciado'
    )
    
    # Contexto
    id_contrato = models.ForeignKey(
        'jobs.Contrato',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_contrato'
    )
    id_mensaje = models.ForeignKey(
        'chats.Mensaje',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_mensaje'
    )
    
    # Detalles
    motivo = models.CharField(max_length=30, choices=MOTIVO_DENUNCIA_CHOICES)
    descripcion = models.TextField()
    evidencia_url = models.CharField(max_length=500, null=True, blank=True)
    
    # Estado
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_DENUNCIA_CHOICES,
        default='pendiente'
    )
    resolucion = models.TextField(null=True, blank=True)
    
    # Moderador
    id_moderador = models.ForeignKey(
        'users.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='denuncias_moderadas',
        db_column='id_moderador'
    )
    
    # Fechas
    fecha = models.DateTimeField(auto_now_add=True)
    fecha_revision = models.DateTimeField(null=True, blank=True)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'denuncia'
        indexes = [
            models.Index(fields=['id_denunciado', 'estado']),
            models.Index(fields=['estado', '-fecha']),
            models.Index(fields=['id_moderador', 'estado']),
        ]


class Disputa(models.Model):
    ESTADO_DISPUTA_CHOICES = [
        ('abierta', 'Abierta'),
        ('en_mediacion', 'En Mediación'),
        ('resuelta', 'Resuelta'),
        ('cerrada', 'Cerrada'),
    ]

    id_disputa = models.AutoField(primary_key=True)
    id_contrato = models.ForeignKey(
        'jobs.Contrato',
        on_delete=models.CASCADE,
        db_column='id_contrato'
    )
    id_iniciada_por = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        related_name='disputas_iniciadas',
        db_column='id_iniciada_por'
    )
    
    # Detalles
    motivo = models.TextField()
    evidencias = models.CharField(max_length=500, null=True, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_DISPUTA_CHOICES,
        default='abierta'
    )
    
    # Resolución
    resolucion = models.TextField(null=True, blank=True)
    monto_resolucion = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    id_favorece_a = models.ForeignKey(
        'users.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='disputas_ganadas',
        db_column='id_favorece_a'
    )
    
    # Mediador
    id_mediador = models.ForeignKey(
        'users.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='disputas_mediadas',
        db_column='id_mediador'
    )
    
    # Fechas
    created_at = models.DateTimeField(auto_now_add=True)
    fecha_revision = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'disputa'
        indexes = [
            models.Index(fields=['id_contrato', 'estado']),
            models.Index(fields=['estado', '-created_at']),
            models.Index(fields=['id_mediador', 'estado']),
        ]


# ==================== NOTIFICACIONES ====================
class Notificacion(models.Model):
    TIPO_NOTIFICACION_CHOICES = [
        ('postulacion', 'Postulación'),
        ('mensaje', 'Mensaje'),
        ('contrato', 'Contrato'),
        ('pago', 'Pago'),
        ('calificacion', 'Calificación'),
        ('sistema', 'Sistema'),
        ('verificacion', 'Verificación'),
    ]

    id_notificacion = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        db_column='id_usuario'
    )
    
    tipo = models.CharField(max_length=20, choices=TIPO_NOTIFICACION_CHOICES)
    titulo = models.CharField(max_length=255)
    mensaje = models.TextField(null=True, blank=True)
    
    # Entidad Relacionada
    entity_tipo = models.CharField(max_length=50, null=True, blank=True)
    entity_id = models.IntegerField(null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    
    # Estado
    leida = models.BooleanField(default=False)
    fecha_leida = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notificacion'
        indexes = [
            models.Index(fields=['id_usuario', 'leida']),
            models.Index(fields=['tipo', '-created_at']),
        ]


# ==================== LOGS Y AUDITORÍA ====================
class LogEvento(models.Model):
    NIVEL_LOG_CHOICES = [
        ('INFO', 'Info'),
        ('WARNING', 'Warning'),
        ('ERROR', 'Error'),
        ('CRITICAL', 'Critical'),
    ]

    id_log = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        'users.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_usuario'
    )
    
    # Detalles del Evento
    accion = models.CharField(max_length=100)
    entidad = models.CharField(max_length=50, null=True, blank=True)
    entidad_id = models.IntegerField(null=True, blank=True)
    nivel = models.CharField(max_length=10, choices=NIVEL_LOG_CHOICES, default='INFO')
    
    # Datos Adicionales
    payload = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'log_evento'
        indexes = [
            models.Index(fields=['id_usuario', '-created_at']),
            models.Index(fields=['accion', '-created_at']),
            models.Index(fields=['nivel', '-created_at']),
            models.Index(fields=['entidad', 'entidad_id']),
        ]