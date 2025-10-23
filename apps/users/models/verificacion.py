"""
Modelos de Verificación y Certificaciones
Responsabilidad: Gestionar verificaciones y certificaciones de usuarios
"""

from django.db import models
from .usuario import Usuario


class Verificacion(models.Model):
    """Verificación de Identidad del Usuario"""
    
    TIPO_VERIFICACION_CHOICES = [
        ('dni', 'DNI'),
        ('antecedentes', 'Antecedentes Penales'),
        ('rostro', 'Verificación Facial'),
        ('telefono', 'Teléfono'),
        ('email', 'Email'),
    ]

    ESTADO_VERIFICACION_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('verificado', 'Verificado'),
        ('rechazado', 'Rechazado'),
        ('expirado', 'Expirado'),
    ]

    id_verificacion = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='verificaciones',
        db_column='id_usuario'
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_VERIFICACION_CHOICES,
        db_index=True
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_VERIFICACION_CHOICES,
        default='pendiente',
        db_index=True
    )
    
    # Archivos
    archivo_url = models.CharField(max_length=500, null=True, blank=True)
    archivo_frontal = models.CharField(max_length=500, null=True, blank=True)
    archivo_posterior = models.CharField(max_length=500, null=True, blank=True)
    
    # Observaciones
    observaciones = models.TextField(null=True, blank=True)
    motivo_rechazo = models.TextField(null=True, blank=True)
    
    # Fechas
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_revision = models.DateTimeField(null=True, blank=True)
    fecha_expiracion = models.DateField(null=True, blank=True)
    
    # Revisor
    id_revisado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verificaciones_revisadas',
        db_column='id_revisado_por'
    )

    class Meta:
        db_table = 'verificacion'
        indexes = [
            models.Index(fields=['id_usuario', 'tipo', 'estado']),
            models.Index(fields=['estado', 'fecha_solicitud'])
        ]
        verbose_name = 'Verificación'
        verbose_name_plural = 'Verificaciones'

    def __str__(self):
        return f"Verificación {self.tipo} de {self.id_usuario.nombre_completo}"

    def aprobar(self, revisor):
        """Aprueba la verificación"""
        from django.utils import timezone
        self.estado = 'verificado'
        self.id_revisado_por = revisor
        self.fecha_revision = timezone.now()
        self.save(update_fields=['estado', 'id_revisado_por', 'fecha_revision'])

    def rechazar(self, revisor, motivo):
        """Rechaza la verificación"""
        from django.utils import timezone
        self.estado = 'rechazado'
        self.id_revisado_por = revisor
        self.motivo_rechazo = motivo
        self.fecha_revision = timezone.now()
        self.save(update_fields=['estado', 'id_revisado_por', 'motivo_rechazo', 'fecha_revision'])


class Certificacion(models.Model):
    """Certificación Profesional del Usuario"""
    
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='certificaciones',
        db_column='id_usuario'
    )
    
    titulo = models.CharField(max_length=255)
    institucion = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    archivo = models.CharField(max_length=500, null=True, blank=True)
    fecha_obtencion = models.DateField(null=True, blank=True)
    fecha_expiracion = models.DateField(null=True, blank=True)
    
    verificada = models.BooleanField(default=False, db_index=True)
    fecha_verificacion = models.DateTimeField(null=True, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'certificacion'
        indexes = [
            models.Index(fields=['id_usuario', 'verificada']),
            models.Index(fields=['-fecha_obtencion'])
        ]
        verbose_name = 'Certificación'
        verbose_name_plural = 'Certificaciones'

    def __str__(self):
        return f"{self.titulo} - {self.id_usuario.nombre_completo}"

    def verificar(self):
        """Marca la certificación como verificada"""
        from django.utils import timezone
        self.verificada = True
        self.fecha_verificacion = timezone.now()
        self.save(update_fields=['verificada', 'fecha_verificacion'])


class TrabajosRealizados(models.Model):
    """Historial de Trabajos Realizados"""
    
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='trabajos_realizados',
        db_column='id_usuario'
    )
    
    titulo = models.CharField(max_length=255)
    empresa = models.CharField(max_length=255, null=True, blank=True)
    rol = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    actualmente = models.BooleanField(
        default=False,
        help_text="Si actualmente trabaja aquí"
    )
    
    referencias = models.TextField(null=True, blank=True)
    documentos = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'trabajos_realizados'
        indexes = [
            models.Index(fields=['id_usuario', '-fecha_inicio'])
        ]
        verbose_name = 'Trabajo Realizado'
        verbose_name_plural = 'Trabajos Realizados'
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.titulo} - {self.id_usuario.nombre_completo}"