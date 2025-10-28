"""
Implementación del Repositorio de Calificación
"""

from typing import List, Optional, Dict, Any
from django.db.models import Avg, Count

from apps.jobs.models import Calificacion
from apps.users.models import Usuario
from .interfaces import ICalificacionRepository


class CalificacionRepository(ICalificacionRepository):
    """
    Repositorio concreto para Calificación
    """
    
    def listar_por_receptor(self, usuario: Usuario) -> List[Calificacion]:
        """Lista calificaciones recibidas por un usuario"""
        return list(
            Calificacion.objects.filter(
                id_receptor=usuario
            ).select_related('id_autor', 'id_contrato')
        )
    
    def listar_por_autor(self, usuario: Usuario) -> List[Calificacion]:
        """Lista calificaciones dadas por un usuario"""
        return list(
            Calificacion.objects.filter(
                id_autor=usuario,
                activa=True
            ).select_related('id_receptor', 'id_contrato').order_by('-fecha')
        )
    
    def obtener_por_contrato(self, contrato, autor: Usuario) -> Optional[Calificacion]:
        """Obtiene calificación de un contrato por un autor"""
        try:
            return Calificacion.objects.get(
                id_contrato=contrato,
                id_autor=autor
            )
        except Calificacion.DoesNotExist:
            return None
    
    def crear(self, datos: Dict[str, Any]) -> Calificacion:
        """Crea una calificación"""
        return Calificacion.objects.create(**datos)
    
    def actualizar(self, calificacion: Calificacion, datos: Dict[str, Any]) -> Calificacion:
        """Actualiza una calificación"""
        for campo, valor in datos.items():
            if hasattr(calificacion, campo):
                setattr(calificacion, campo, valor)
        
        calificacion.editada = True
        calificacion.save()
        return calificacion
    
    def desactivar(self, calificacion_id: int) -> bool:
        """Desactiva una calificación"""
        try:
            calificacion = Calificacion.objects.get(id_calificacion=calificacion_id)
            calificacion.activa = False
            calificacion.save(update_fields=['activa'])
            return True
        except Calificacion.DoesNotExist:
            return False
    
    def calcular_estadisticas(self, usuario: Usuario) -> Dict[str, Any]:
        """Calcula estadísticas de calificaciones"""
        calificaciones = Calificacion.objects.filter(
            id_receptor=usuario,
            activa=True
        )
        
        total = calificaciones.count()
        
        if total == 0:
            return {
                'total': 0,
                'promedio': 0.00,
                'estrellas': {i: 0 for i in range(1, 6)},
                'promedio_puntualidad': None,
                'promedio_calidad': None,
                'promedio_comunicacion': None,
            }
        
        # Calcular promedio general
        suma = sum(cal.puntuacion for cal in calificaciones)
        promedio = round(suma / total, 2)
        
        # Contar por estrellas
        estrellas = {i: 0 for i in range(1, 6)}
        for cal in calificaciones:
            estrellas[cal.puntuacion] += 1
        
        # Calcular promedios de aspectos detallados
        calificaciones_con_detalles = calificaciones.exclude(
            puntualidad__isnull=True,
            calidad_trabajo__isnull=True,
            comunicacion__isnull=True
        )
        
        promedios_detallados = {}
        if calificaciones_con_detalles.exists():
            promedios = calificaciones_con_detalles.aggregate(
                Avg('puntualidad'),
                Avg('calidad_trabajo'),
                Avg('comunicacion')
            )
            promedios_detallados = {
                'promedio_puntualidad': round(promedios['puntualidad__avg'], 1) if promedios['puntualidad__avg'] else None,
                'promedio_calidad': round(promedios['calidad_trabajo__avg'], 1) if promedios['calidad_trabajo__avg'] else None,
                'promedio_comunicacion': round(promedios['comunicacion__avg'], 1) if promedios['comunicacion__avg'] else None,
            }
        else:
            promedios_detallados = {
                'promedio_puntualidad': None,
                'promedio_calidad': None,
                'promedio_comunicacion': None,
            }
        
        return {
            'total': total,
            'promedio': promedio,
            'estrellas': estrellas,
            **promedios_detallados
        }
    
    def obtener_ultimas(self, usuario: Usuario, limite: int = 10) -> List[Calificacion]:
        """Obtiene las últimas N calificaciones"""
        return list(
            Calificacion.objects.filter(
                id_receptor=usuario,
                activa=True
            ).select_related('id_autor').order_by('-fecha')[:limite]
        )