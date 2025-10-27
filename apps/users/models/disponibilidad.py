"""
Modelo de Disponibilidad - Simplificado
"""
from django.db import models


class Disponibilidad(models.Model):
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
        'Usuario',
        on_delete=models.CASCADE,
        related_name='disponibilidad_set'
    )
    
    dia_semana = models.IntegerField(choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    activa = models.BooleanField(default=True)

    class Meta:
        db_table = 'disponibilidad'
        unique_together = [['id_trabajador', 'dia_semana', 'hora_inicio', 'hora_fin']]
        verbose_name = 'Disponibilidad'
        verbose_name_plural = 'Disponibilidades'
        ordering = ['dia_semana', 'hora_inicio']

    def __str__(self):
        dia = dict(self.DIAS_SEMANA)[self.dia_semana]
        return f"{self.id_trabajador.nombre_completo} - {dia} {self.hora_inicio}-{self.hora_fin}"