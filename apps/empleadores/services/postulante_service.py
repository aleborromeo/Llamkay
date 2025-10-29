"""
Servicio de Postulantes para Empleadores
Responsabilidad: Lógica de negocio para gestión de postulantes
"""
from typing import Dict, List, Optional
from apps.jobs.repositories import PostulacionRepository


class PostulanteService:
    """
    Servicio para gestión de postulantes desde perspectiva del empleador
    Principio de Responsabilidad Única (SOLID)
    """
    
    def __init__(self):
        self.postulacion_repo = PostulacionRepository()
    
    def get_postulantes_oferta(
        self,
        oferta_id: int,
        tipo_oferta: str,
        empleador_id: int,
        estado: Optional[str] = None
    ) -> Dict:
        """
        Obtiene los postulantes de una oferta
        
        Args:
            oferta_id: ID de la oferta
            tipo_oferta: 'usuario' o 'empresa'
            empleador_id: ID del empleador (validación)
            estado: Filtro opcional por estado
        
        Returns:
            Dict con postulaciones y estadísticas
        """
        # Obtener postulaciones
        postulaciones = self.postulacion_repo.get_postulaciones_oferta(
            oferta_id,
            tipo_oferta
        )
        
        # Filtrar por estado si es necesario
        if estado:
            postulaciones = postulaciones.filter(estado=estado)
        
        # Formatear postulaciones
        postulaciones_data = []
        for post in postulaciones:
            postulaciones_data.append({
                'id': post.id_postulacion,
                'trabajador': {
                    'id': post.id_trabajador.id_usuario,
                    'nombre': post.id_trabajador.nombre_completo,
                },
                'mensaje': post.mensaje,
                'pretension_salarial': post.pretension_salarial,
                'disponibilidad_inmediata': post.disponibilidad_inmediata,
                'estado': post.estado,
                'estado_display': post.get_estado_display(),
                'leida': post.leida,
                'fecha_postulacion': post.created_at,
            })
        
        # Calcular estadísticas
        total = len(postulaciones_data)
        pendientes = sum(1 for p in postulaciones_data if p['estado'] == 'pendiente')
        aceptadas = sum(1 for p in postulaciones_data if p['estado'] == 'aceptada')
        rechazadas = sum(1 for p in postulaciones_data if p['estado'] == 'rechazada')
        
        return {
            'postulaciones': postulaciones_data,
            'estadisticas': {
                'total': total,
                'pendientes': pendientes,
                'aceptadas': aceptadas,
                'rechazadas': rechazadas,
            }
        }
    
    def aceptar_postulante(
        self,
        postulacion_id: int,
        empleador_id: int
    ) -> Dict:
        """
        Acepta una postulación
        
        Args:
            postulacion_id: ID de la postulación
            empleador_id: ID del empleador (validación)
        
        Returns:
            Dict con 'success' y 'message'
        """
        postulacion = self.postulacion_repo.get_by_id(postulacion_id)
        
        if not postulacion:
            return {
                'success': False,
                'message': 'Postulación no encontrada'
            }
        
        # Validar que sea el dueño de la oferta
        oferta = postulacion.oferta
        if oferta.id_empleador.id_usuario != empleador_id:
            return {
                'success': False,
                'message': 'No tienes permisos para esta acción'
            }
        
        # Cambiar estado
        if self.postulacion_repo.actualizar_estado(postulacion_id, 'aceptada'):
            # TODO: Crear notificación para el trabajador
            return {
                'success': True,
                'message': 'Postulación aceptada correctamente'
            }
        
        return {
            'success': False,
            'message': 'Error al aceptar postulación'
        }
    
    def rechazar_postulante(
        self,
        postulacion_id: int,
        empleador_id: int
    ) -> Dict:
        """
        Rechaza una postulación
        
        Args:
            postulacion_id: ID de la postulación
            empleador_id: ID del empleador (validación)
        
        Returns:
            Dict con 'success' y 'message'
        """
        postulacion = self.postulacion_repo.get_by_id(postulacion_id)
        
        if not postulacion:
            return {
                'success': False,
                'message': 'Postulación no encontrada'
            }
        
        # Validar que sea el dueño de la oferta
        oferta = postulacion.oferta
        if oferta.id_empleador.id_usuario != empleador_id:
            return {
                'success': False,
                'message': 'No tienes permisos para esta acción'
            }
        
        # Cambiar estado
        if self.postulacion_repo.actualizar_estado(postulacion_id, 'rechazada'):
            # TODO: Crear notificación para el trabajador
            return {
                'success': True,
                'message': 'Postulación rechazada'
            }
        
        return {
            'success': False,
            'message': 'Error al rechazar postulación'
        }
    
    def get_postulaciones_recientes(
        self,
        empleador_id: int,
        limit: int = 10
    ) -> List[Dict]:
        """
        Obtiene las postulaciones más recientes del empleador
        
        Args:
            empleador_id: ID del empleador
            limit: Límite de resultados
        
        Returns:
            Lista de postulaciones formateadas
        """
        postulaciones = self.postulacion_repo.get_postulaciones_empleador(
            empleador_id
        )[:limit]
        
        postulaciones_data = []
        for post in postulaciones:
            oferta = post.oferta
            tipo = post.tipo_oferta
            
            postulaciones_data.append({
                'id': post.id_postulacion,
                'tipo': tipo,
                'titulo': oferta.titulo if tipo == 'usuario' else oferta.titulo_puesto,
                'trabajador': post.id_trabajador.nombre_completo,
                'estado': post.estado,
                'estado_display': post.get_estado_display(),
                'fecha': post.created_at,
                'leida': post.leida,
                'oferta_id': oferta.id,
            })
        
        return postulaciones_data
    
    def get_estadisticas_postulaciones(self, empleador_id: int) -> Dict:
        """
        Obtiene estadísticas de postulaciones del empleador
        
        Args:
            empleador_id: ID del empleador
        
        Returns:
            Dict con estadísticas
        """
        contadores = self.postulacion_repo.contar_postulaciones_empleador(empleador_id)
        
        return {
            'total_postulaciones': contadores['total'],
            'postulaciones_pendientes': contadores['pendientes'],
            'postulaciones_aceptadas': contadores['aceptadas'],
            'postulaciones_rechazadas': contadores['rechazadas'],
        }