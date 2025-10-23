"""
Modelo de Disponibilidad
Responsabilidad: Gestionar horarios disponibles del trabajador
"""

from django.db import models
from .usuario import Usuario


class Disponibilidad(models.Model):
    """Disponibilidad Horaria del Trabajador"""
    
    DIAS_SEMANA = [
        (0, 'Domingo'),
        (1, 'Lunes'),
        (2, 'Martes'),
        (3, 'Miércoles'),
        (4, 'Jueves'),
        (5, 'Viernes'),
        (6, 'Sábado'),
    ]

    id = models.AutoField(primary_key=True)
    id_trabajador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='disponibilidad_set',
        db_column='id_trabajador'
    )
    
    dia_semana = models.IntegerField(
        choices=DIAS_SEMANA,
        help_text="0=Domingo, 1=Lunes, ..., 6=Sábado"
    )
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    activa = models.BooleanField(default=True, db_index=True)

    class Meta:
        db_table = 'disponibilidad'
        unique_together = [['id_trabajador', 'dia_semana', 'hora_inicio', 'hora_fin']]
        indexes = [
            models.Index(fields=['id_trabajador', 'dia_semana', 'activa'])
        ]
        verbose_name = 'Disponibilidad'
        verbose_name_plural = 'Disponibilidades'
        ordering = ['dia_semana', 'hora_inicio']

    def __str__(self):
        dia = dict(self.DIAS_SEMANA)[self.dia_semana]
        return f"{self.id_trabajador.nombre_completo} - {dia} {self.hora_inicio}-{self.hora_fin}"

    def desactivar(self):
        """Desactiva la disponibilidad"""
        self.activa = False
        self.save(update_fields=['activa'])