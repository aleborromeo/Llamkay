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
        try:
            print("="*80)
            print(f"🟢 ACEPTAR POSTULANTE - ID: {postulacion_id}, Empleador: {empleador_id}")
            
            postulacion = self.postulacion_repo.get_by_id(postulacion_id)
            
            if not postulacion:
                print("❌ Postulación no encontrada")
                return {
                    'success': False,
                    'message': 'Postulación no encontrada'
                }
            
            print(f"✅ Postulación encontrada - Estado actual: {postulacion.estado}")
            
            # Obtener la oferta según el tipo usando los nombres correctos de los campos
            if postulacion.id_oferta_usuario:
                oferta = postulacion.id_oferta_usuario
                oferta_empleador_id = oferta.id_empleador.id_usuario
                print(f"📋 Oferta Usuario - ID: {oferta.id}, Empleador: {oferta_empleador_id}")
            elif postulacion.id_oferta_empresa:
                oferta = postulacion.id_oferta_empresa
                oferta_empleador_id = oferta.id_empleador.id_usuario
                print(f"📋 Oferta Empresa - ID: {oferta.id}, Empleador: {oferta_empleador_id}")
            else:
                print("❌ No se encontró oferta asociada")
                return {
                    'success': False,
                    'message': 'No se encontró la oferta asociada a esta postulación'
                }
            
            # Validar que sea el dueño de la oferta
            if oferta_empleador_id != empleador_id:
                print(f"❌ Sin permisos - Empleador oferta: {oferta_empleador_id}, Empleador actual: {empleador_id}")
                return {
                    'success': False,
                    'message': 'No tienes permisos para esta acción'
                }
            
            # Verificar que no esté ya aceptada
            if postulacion.estado == 'aceptada':
                print("⚠️ Ya estaba aceptada")
                return {
                    'success': False,
                    'message': 'Esta postulación ya fue aceptada'
                }
            
            # Cambiar estado
            print(f"🔄 Actualizando estado de {postulacion.estado} a 'aceptada'")
            if self.postulacion_repo.actualizar_estado(postulacion_id, 'aceptada'):
                print("✅ Estado actualizado correctamente")
                # TODO: Crear notificación para el trabajador
                return {
                    'success': True,
                    'message': 'Postulación aceptada correctamente'
                }
            
            print("❌ Error al actualizar estado")
            return {
                'success': False,
                'message': 'Error al aceptar postulación'
            }
            
        except Exception as e:
            print(f"💥 ERROR CRÍTICO en aceptar_postulante: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'message': f'Error interno: {str(e)}'
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
        try:
            print("="*80)
            print(f"🔴 RECHAZAR POSTULANTE - ID: {postulacion_id}, Empleador: {empleador_id}")
            
            postulacion = self.postulacion_repo.get_by_id(postulacion_id)
            
            if not postulacion:
                print("❌ Postulación no encontrada")
                return {
                    'success': False,
                    'message': 'Postulación no encontrada'
                }
            
            print(f"✅ Postulación encontrada - Estado actual: {postulacion.estado}")
            
            # Obtener la oferta según el tipo usando los nombres correctos de los campos
            if postulacion.id_oferta_usuario:
                oferta = postulacion.id_oferta_usuario
                oferta_empleador_id = oferta.id_empleador.id_usuario
                print(f"📋 Oferta Usuario - ID: {oferta.id}, Empleador: {oferta_empleador_id}")
            elif postulacion.id_oferta_empresa:
                oferta = postulacion.id_oferta_empresa
                oferta_empleador_id = oferta.id_empleador.id_usuario
                print(f"📋 Oferta Empresa - ID: {oferta.id}, Empleador: {oferta_empleador_id}")
            else:
                print("❌ No se encontró oferta asociada")
                return {
                    'success': False,
                    'message': 'No se encontró la oferta asociada a esta postulación'
                }
            
            # Validar que sea el dueño de la oferta
            if oferta_empleador_id != empleador_id:
                print(f"❌ Sin permisos - Empleador oferta: {oferta_empleador_id}, Empleador actual: {empleador_id}")
                return {
                    'success': False,
                    'message': 'No tienes permisos para esta acción'
                }
            
            # Verificar que no esté ya rechazada
            if postulacion.estado == 'rechazada':
                print("⚠️ Ya estaba rechazada")
                return {
                    'success': False,
                    'message': 'Esta postulación ya fue rechazada'
                }
            
            # Cambiar estado
            print(f"🔄 Actualizando estado de {postulacion.estado} a 'rechazada'")
            if self.postulacion_repo.actualizar_estado(postulacion_id, 'rechazada'):
                print("✅ Estado actualizado correctamente")
                # TODO: Crear notificación para el trabajador
                return {
                    'success': True,
                    'message': 'Postulación rechazada correctamente'
                }
            
            print("❌ Error al actualizar estado")
            return {
                'success': False,
                'message': 'Error al rechazar postulación'
            }
            
        except Exception as e:
            print(f"💥 ERROR CRÍTICO en rechazar_postulante: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'message': f'Error interno: {str(e)}'
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
            # Obtener oferta según los campos correctos
            if post.id_oferta_usuario:
                oferta = post.id_oferta_usuario
                tipo = 'usuario'
                titulo = oferta.titulo
            else:
                oferta = post.id_oferta_empresa
                tipo = 'empresa'
                titulo = oferta.titulo_puesto if oferta else 'Oferta eliminada'
            
            postulaciones_data.append({
                'id': post.id_postulacion,
                'tipo': tipo,
                'titulo': titulo,
                'trabajador': post.id_trabajador.nombre_completo,
                'estado': post.estado,
                'estado_display': post.get_estado_display(),
                'fecha': post.created_at,
                'leida': post.leida,
                'oferta_id': oferta.id if oferta else None,
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