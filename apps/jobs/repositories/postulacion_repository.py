"""
Repositorio de Postulaciones
Agrega estos métodos a tu PostulacionRepository
"""
from typing import Optional
from django.db.models import QuerySet
from apps.jobs.models import Postulacion


class PostulacionRepository:
    """Repositorio para gestión de postulaciones"""
    
    @staticmethod
    def get_by_id(postulacion_id: int) -> Optional[Postulacion]:
        """
        Obtiene una postulación por ID con sus relaciones
        
        Args:
            postulacion_id: ID de la postulación
        
        Returns:
            Postulacion o None
        """
        try:
            return Postulacion.objects.select_related(
                'id_trabajador',
                'id_oferta_usuario',
                'id_oferta_usuario__id_empleador',
                'id_oferta_empresa',
                'id_oferta_empresa__id_empleador'
            ).get(id_postulacion=postulacion_id)
        except Postulacion.DoesNotExist:
            print(f"❌ Postulación {postulacion_id} no existe")
            return None
    
    @staticmethod
    def actualizar_estado(postulacion_id: int, nuevo_estado: str) -> bool:
        """
        Actualiza el estado de una postulación
        
        Args:
            postulacion_id: ID de la postulación
            nuevo_estado: Nuevo estado ('pendiente', 'aceptada', 'rechazada', etc.)
        
        Returns:
            bool: True si se actualizó correctamente, False si no
        """
        try:
            postulacion = Postulacion.objects.get(id_postulacion=postulacion_id)
            estado_anterior = postulacion.estado
            
            postulacion.estado = nuevo_estado
            postulacion.save(update_fields=['estado', 'updated_at'])
            
            print(f"✅ Postulación {postulacion_id}: {estado_anterior} -> {nuevo_estado}")
            return True
            
        except Postulacion.DoesNotExist:
            print(f"❌ Postulación {postulacion_id} no encontrada para actualizar estado")
            return False
        except Exception as e:
            print(f"❌ Error al actualizar estado de postulación {postulacion_id}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    @staticmethod
    def get_postulaciones_oferta(oferta_id: int, tipo_oferta: str) -> QuerySet:
        """
        Obtiene todas las postulaciones de una oferta
        
        Args:
            oferta_id: ID de la oferta
            tipo_oferta: 'usuario' o 'empresa'
        
        Returns:
            QuerySet de postulaciones
        """
        if tipo_oferta == 'usuario':
            return Postulacion.objects.filter(
                id_oferta_usuario_id=oferta_id
            ).select_related(
                'id_trabajador'
            ).order_by('-created_at')
        else:
            return Postulacion.objects.filter(
                id_oferta_empresa_id=oferta_id
            ).select_related(
                'id_trabajador'
            ).order_by('-created_at')
    
    @staticmethod
    def get_postulaciones_empleador(empleador_id: int) -> QuerySet:
        """
        Obtiene todas las postulaciones de las ofertas de un empleador
        
        Args:
            empleador_id: ID del empleador
        
        Returns:
            QuerySet de postulaciones
        """
        from django.db.models import Q
        
        return Postulacion.objects.filter(
            Q(id_oferta_usuario__id_empleador_id=empleador_id) |
            Q(id_oferta_empresa__id_empleador_id=empleador_id)
        ).select_related(
            'id_trabajador',
            'id_oferta_usuario',
            'id_oferta_empresa'
        ).order_by('-created_at')
    
    @staticmethod
    def contar_postulaciones_empleador(empleador_id: int) -> dict:
        """
        Cuenta las postulaciones por estado de un empleador
        
        Args:
            empleador_id: ID del empleador
        
        Returns:
            Dict con contadores
        """
        from django.db.models import Q, Count
        
        postulaciones = Postulacion.objects.filter(
            Q(id_oferta_usuario__id_empleador_id=empleador_id) |
            Q(id_oferta_empresa__id_empleador_id=empleador_id)
        )
        
        return {
            'total': postulaciones.count(),
            'pendientes': postulaciones.filter(estado='pendiente').count(),
            'aceptadas': postulaciones.filter(estado='aceptada').count(),
            'rechazadas': postulaciones.filter(estado='rechazada').count(),
        }