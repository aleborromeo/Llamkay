"""
Modelo de Postulaciones
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class Postulacion(models.Model):
    """
    Postulaciones de trabajadores a ofertas
    """
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En Revisión'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]

    id_postulacion = models.AutoField(primary_key=True)
    id_trabajador = models.ForeignKey(
        'users.Usuario', 
        on_delete=models.CASCADE,
        related_name='postulaciones_realizadas'
    )
    id_oferta_usuario = models.ForeignKey(
        'jobs.OfertaUsuario', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='postulaciones'
    )
    id_oferta_empresa = models.ForeignKey(
        'jobs.OfertaEmpresa', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='postulaciones'
    )
    
    # Información de la postulación
    mensaje = models.TextField(null=True, blank=True)
    pretension_salarial = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    disponibilidad_inmediata = models.BooleanField(default=False)
    
    # Estado
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    leida = models.BooleanField(default=False)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'postulacion'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['id_trabajador', 'estado']),
            models.Index(fields=['id_oferta_usuario', 'estado']),
            models.Index(fields=['id_oferta_empresa', 'estado']),
            models.Index(fields=['estado', '-created_at']),
        ]
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(id_oferta_usuario__isnull=False, id_oferta_empresa__isnull=True) |
                    models.Q(id_oferta_usuario__isnull=True, id_oferta_empresa__isnull=False)
                ),
                name='postulacion_una_oferta'
            )
        ]
        verbose_name = 'Postulación'
        verbose_name_plural = 'Postulaciones'

    def __str__(self):
        oferta = self.id_oferta_usuario or self.id_oferta_empresa
        return f"{self.id_trabajador.nombre_completo} -> {oferta}"

    @property
    def oferta(self):
        """Retorna la oferta relacionada"""
        return self.id_oferta_usuario or self.id_oferta_empresa

    @property
    def tipo_oferta(self):
        """Retorna el tipo de oferta"""
        return 'usuario' if self.id_oferta_usuario else 'empresa'

    def marcar_como_leida(self):
        """Marca la postulación como leída"""
        if not self.leida:
            self.leida = True
            self.save(update_fields=['leida'])