"""
Modelos de Contratos y Pagos
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


class Contrato(models.Model):
    """
    Contratos entre empleadores y trabajadores
    """
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('activo', 'Activo'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    id_contrato = models.AutoField(primary_key=True)
    id_empleador = models.ForeignKey(
        'users.Usuario',
        on_delete=models.RESTRICT,
        related_name='contratos_como_empleador'
    )
    id_trabajador = models.ForeignKey(
        'users.Usuario',
        on_delete=models.RESTRICT,
        related_name='contratos_como_trabajador'
    )
    id_postulacion = models.ForeignKey(
        'jobs.Postulacion', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='contratos'
    )
    
    # Detalles del contrato
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    precio_acordado = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    moneda = models.CharField(max_length=3, default='PEN')
    
    # Fechas
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin_estimada = models.DateField(null=True, blank=True)
    fecha_fin_real = models.DateField(null=True, blank=True)
    
    # Estado
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contrato'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['id_empleador', 'estado']),
            models.Index(fields=['id_trabajador', 'estado']),
            models.Index(fields=['estado', '-created_at']),
        ]
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'

    def __str__(self):
        return f"Contrato #{self.id_contrato} - {self.titulo}"

    @property
    def esta_activo(self):
        """Verifica si el contrato está activo"""
        return self.estado == 'activo'


class Pago(models.Model):
    """
    Pagos asociados a contratos
    """
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('fallido', 'Fallido'),
        ('reembolsado', 'Reembolsado'),
    ]

    id_pago = models.AutoField(primary_key=True)
    id_contrato = models.ForeignKey(
        Contrato, 
        on_delete=models.RESTRICT,
        related_name='pagos'
    )
    
    # Montos
    monto_total = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    monto_trabajador = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    comision = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    moneda = models.CharField(max_length=3, default='PEN')
    
    # Estado
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pago'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['id_contrato', 'estado']),
            models.Index(fields=['estado', '-created_at']),
        ]
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'

    def __str__(self):
        return f"Pago #{self.id_pago} - {self.monto_total} {self.moneda}"


class Calificacion(models.Model):
    """
    Calificaciones mutuas entre empleadores y trabajadores
    """
    id_calificacion = models.AutoField(primary_key=True)
    id_contrato = models.ForeignKey(
        Contrato, 
        on_delete=models.CASCADE,
        related_name='calificaciones'
    )
    id_autor = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        related_name='calificaciones_dadas'
    )
    id_receptor = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        related_name='calificaciones_recibidas'
    )
    
    # Calificación
    puntuacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.TextField(null=True, blank=True)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'calificacion'
        unique_together = [['id_contrato', 'id_autor']]
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['id_receptor', '-created_at']),
            models.Index(fields=['id_autor', '-created_at']),
        ]
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'

    def __str__(self):
        return f"Calificación {self.puntuacion}★ de {self.id_autor.nombre_completo}"