"""
Servicio de Estadísticas
Responsabilidad: Cálculos y actualización de estadísticas
"""

from typing import Dict, Any
from decimal import Decimal

from apps.users.models import Usuario, UsuarioEstadisticas
from apps.users.repositories import CalificacionRepository


class EstadisticaService:
    """
    Servicio especializado en cálculos estadísticos
    Separado para cumplir SRP
    """
    
    def __init__(self, calificacion_repo: CalificacionRepository = None):
        self.calificacion_repo = calificacion_repo or CalificacionRepository()
    
    def calcular_usuario(self, usuario: Usuario) -> Dict[str, Any]:
        """
        Calcula todas las estadísticas de un usuario
        """
        # Obtener o crear estadísticas
        estadisticas, created = UsuarioEstadisticas.objects.get_or_create(
            id_usuario=usuario,
            defaults={
                'rating_promedio': Decimal('0.00'),
                'total_calificaciones': 0,
                'trabajos_completados': 0,
                'trabajos_activos': 0,
            }
        )
        
        return {
            'trabajos_completados': estadisticas.trabajos_completados,
            'trabajos_activos': estadisticas.trabajos_activos,
            'trabajos_cancelados': estadisticas.trabajos_cancelados,
            'rating_promedio': float(estadisticas.rating_promedio),
            'total_calificaciones': estadisticas.total_calificaciones,
            'ingresos_totales': float(estadisticas.ingresos_totales),
            'ingresos_mes': float(estadisticas.ingresos_mes_actual),
        }
    
    def actualizar_calificaciones(self, usuario: Usuario) -> None:
        """
        Actualiza las estadísticas de calificaciones de un usuario
        Se ejecuta después de crear/actualizar/eliminar una calificación
        """
        # Calcular estadísticas usando el repositorio
        stats = self.calificacion_repo.calcular_estadisticas(usuario)
        
        # Obtener o crear registro de estadísticas
        estadisticas, _ = UsuarioEstadisticas.objects.get_or_create(
            id_usuario=usuario,
            defaults={
                'rating_promedio': Decimal('0.00'),
                'total_calificaciones': 0,
            }
        )
        
        # Actualizar rating
        estadisticas.actualizar_rating(
            nuevo_promedio=Decimal(str(stats['promedio'])),
            total=stats['total']
        )
    
    def incrementar_trabajo_completado(self, usuario: Usuario) -> None:
        """
        Incrementa el contador de trabajos completados
        """
        estadisticas, _ = UsuarioEstadisticas.objects.get_or_create(
            id_usuario=usuario,
            defaults={'trabajos_completados': 0}
        )
        
        estadisticas.incrementar_trabajos_completados()
    
    def actualizar_ingresos(self, usuario: Usuario, monto: Decimal) -> None:
        """
        Actualiza los ingresos del usuario
        """
        estadisticas, _ = UsuarioEstadisticas.objects.get_or_create(
            id_usuario=usuario,
            defaults={
                'ingresos_totales': Decimal('0.00'),
                'ingresos_mes_actual': Decimal('0.00'),
            }
        )
        
        estadisticas.ingresos_totales += monto
        estadisticas.ingresos_mes_actual += monto
        estadisticas.save(update_fields=[
            'ingresos_totales',
            'ingresos_mes_actual',
            'ultima_actualizacion'
        ])
    
    def resetear_ingresos_mes(self, usuario: Usuario) -> None:
        """
        Resetea los ingresos del mes actual
        Debe ejecutarse al inicio de cada mes
        """
        try:
            estadisticas = UsuarioEstadisticas.objects.get(id_usuario=usuario)
            estadisticas.ingresos_mes_actual = Decimal('0.00')
            estadisticas.save(update_fields=['ingresos_mes_actual', 'ultima_actualizacion'])
        except UsuarioEstadisticas.DoesNotExist:
            pass