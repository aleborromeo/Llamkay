"""
Modelos de Soporte - Simplificado
"""
from django.db import models


class Denuncia(models.Model):
    MOTIVO_CHOICES = [
        ('fraude', 'Fraude'),
        ('acoso', 'Acoso'),
        ('spam', 'Spam'),
        ('otro', 'Otro'),
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En Revisión'),
        ('resuelta', 'Resuelta'),
        ('cerrada', 'Cerrada'),
    ]

    id_denuncia = models.AutoField(primary_key=True)
    id_reportante = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        related_name='denuncias_realizadas'
    )
    id_denunciado = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        related_name='denuncias_recibidas'
    )
    
    # Detalles
    motivo = models.CharField(max_length=30, choices=MOTIVO_CHOICES)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    resolucion = models.TextField(null=True, blank=True)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'denuncia'
        verbose_name = 'Denuncia'
        verbose_name_plural = 'Denuncias'

    def __str__(self):
        return f"Denuncia #{self.id_denuncia}"


class Notificacion(models.Model):
    TIPO_CHOICES = [
        ('postulacion', 'Postulación'),
        ('mensaje', 'Mensaje'),
        ('contrato', 'Contrato'),
        ('pago', 'Pago'),
        ('sistema', 'Sistema'),
    ]

    id_notificacion = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        related_name='notificaciones'
    )
    
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    titulo = models.CharField(max_length=255)
    mensaje = models.TextField(null=True, blank=True)
    url = models.CharField(max_length=255, null=True, blank=True)
    
    # Estado
    leida = models.BooleanField(default=False)
    fecha_leida = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'notificacion'
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.titulo}"