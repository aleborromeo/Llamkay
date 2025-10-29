"""
Modelo de Trabajos Guardados
"""
from django.db import models


class GuardarTrabajo(models.Model):
    """
    Trabajos guardados por los usuarios
    """
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        'users.Usuario', 
        on_delete=models.CASCADE,
        related_name='trabajos_guardados'
    )
    id_oferta_usuario = models.ForeignKey(
        'jobs.OfertaUsuario', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='guardados'
    )
    id_oferta_empresa = models.ForeignKey(
        'jobs.OfertaEmpresa', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='guardados'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'guardar_trabajo'
        ordering = ['-created_at']
        unique_together = [
            ['id_usuario', 'id_oferta_usuario'],
            ['id_usuario', 'id_oferta_empresa'],
        ]
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(id_oferta_usuario__isnull=False, id_oferta_empresa__isnull=True) |
                    models.Q(id_oferta_usuario__isnull=True, id_oferta_empresa__isnull=False)
                ),
                name='guardado_una_oferta'
            )
        ]
        indexes = [
            models.Index(fields=['id_usuario', '-created_at']),
        ]
        verbose_name = 'Trabajo Guardado'
        verbose_name_plural = 'Trabajos Guardados'

    def __str__(self):
        oferta = self.id_oferta_usuario or self.id_oferta_empresa
        return f"{self.id_usuario.nombre_completo} guardó {oferta}"

    @property
    def oferta(self):
        """Retorna la oferta guardada"""
        return self.id_oferta_usuario or self.id_oferta_empresa

    @property
    def tipo_oferta(self):
        """Retorna el tipo de oferta guardada"""
        return 'usuario' if self.id_oferta_usuario else 'empresa'