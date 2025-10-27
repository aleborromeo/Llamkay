"""
Modelos de Verificación - Simplificado
"""
from django.db import models


class Verificacion(models.Model):
    TIPO_CHOICES = [
        ('dni', 'DNI'),
        ('telefono', 'Teléfono'),
        ('email', 'Email'),
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('verificado', 'Verificado'),
        ('rechazado', 'Rechazado'),
    ]

    id_verificacion = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,
        related_name='verificaciones'
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    
    # Archivos
    archivo_url = models.CharField(max_length=500, null=True, blank=True)
    
    # Observaciones
    observaciones = models.TextField(null=True, blank=True)
    motivo_rechazo = models.TextField(null=True, blank=True)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    fecha_revision = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'verificacion'
        verbose_name = 'Verificación'
        verbose_name_plural = 'Verificaciones'

    def __str__(self):
        return f"Verificación {self.tipo} - {self.id_usuario.nombre_completo}"


class Certificacion(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,
        related_name='certificaciones'
    )
    
    titulo = models.CharField(max_length=255)
    institucion = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    archivo = models.CharField(max_length=500, null=True, blank=True)
    fecha_obtencion = models.DateField(null=True, blank=True)
    
    verificada = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'certificacion'
        verbose_name = 'Certificación'
        verbose_name_plural = 'Certificaciones'

    def __str__(self):
        return f"{self.titulo} - {self.id_usuario.nombre_completo}"


class TrabajosRealizados(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,
        related_name='trabajos_realizados'
    )
    
    titulo = models.CharField(max_length=255)
    empresa = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    actualmente = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'trabajos_realizados'
        verbose_name = 'Trabajo Realizado'
        verbose_name_plural = 'Trabajos Realizados'
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.titulo} - {self.id_usuario.nombre_completo}"