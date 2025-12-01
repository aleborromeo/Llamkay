"""
Servicio de Postulaciones
Responsabilidad: Lógica de negocio para postulaciones
"""
from typing import Dict, List, Optional
from decimal import Decimal
from apps.jobs.repositories import PostulacionRepository, OfertaRepository


class PostulacionService:
    """
    Servicio para gestión de postulaciones
    Principio de Responsabilidad Única (SOLID)
    """
    
    def __init__(self):
        self.postulacion_repo = PostulacionRepository()
        self.oferta_repo = OfertaRepository()
    
    def crear_postulacion(
        self,
        trabajador_id: int,
        oferta_id: int,
        tipo_oferta: str,
        mensaje: str,
        pretension_salarial: Optional[Decimal] = None,
        disponibilidad_inmediata: bool = False
    ) -> Dict:
        """
        Crea una nueva postulación
        
        Args:
            trabajador_id: ID del trabajador
            oferta_id: ID de la oferta
            tipo_oferta: 'usuario' o 'empresa'
            mensaje: Mensaje de presentación
            pretension_salarial: Pretensión salarial (opcional)
            disponibilidad_inmediata: Tiene disponibilidad inmediata
        
        Returns:
            Dict con 'success' y 'message' o 'postulacion'
        """
        # Validar que la oferta existe y está activa
        if tipo_oferta == 'usuario':
            oferta = self.oferta_repo.get_oferta_usuario_by_id(oferta_id)
        else:
            oferta = self.oferta_repo.get_oferta_empresa_by_id(oferta_id)
        
        if not oferta:
            return {'success': False, 'message': 'Oferta no encontrada'}
        
        if oferta.estado != 'activa':
            return {'success': False, 'message': 'La oferta no está activa'}
        
        # Verificar que no sea el dueño
        if oferta.id_empleador.id_usuario == trabajador_id:
            return {'success': False, 'message': 'No puedes postular a tu propia oferta'}
        
        # Verificar que no haya postulado antes
        if self.postulacion_repo.existe_postulacion(trabajador_id, oferta_id, tipo_oferta):
            return {'success': False, 'message': 'Ya postulaste a esta oferta'}
        
        # Crear postulación
        datos = {
            'id_trabajador_id': trabajador_id,
            'mensaje': mensaje,
            'disponibilidad_inmediata': disponibilidad_inmediata,
            'estado': 'pendiente',
        }
        
        if tipo_oferta == 'usuario':
            datos['id_oferta_usuario_id'] = oferta_id
        else:
            datos['id_oferta_empresa_id'] = oferta_id
        
        if pretension_salarial:
            datos['pretension_salarial'] = pretension_salarial
        
        postulacion = self.postulacion_repo.crear_postulacion(datos)
        
        return {
            'success': True,
            'message': 'Postulación enviada exitosamente',
            'postulacion': postulacion
        }
    
    def get_postulaciones_trabajador(
        self,
        trabajador_id: int,
        estado: Optional[str] = None
    ) -> List[Dict]:
        """
        Obtiene las postulaciones de un trabajador
        
        Args:
            trabajador_id: ID del trabajador
            estado: Filtro opcional por estado
        
        Returns:
            Lista de postulaciones formateadas
        """
        postulaciones = self.postulacion_repo.get_postulaciones_trabajador(
            trabajador_id,
            estado
        )
        
        return [self._formatear_postulacion(p) for p in postulaciones]
    
    def retirar_postulacion(
        self,
        postulacion_id: int,
        trabajador_id: int
    ) -> Dict:
        """
        Retira una postulación
        
        Args:
            postulacion_id: ID de la postulación
            trabajador_id: ID del trabajador (validación)
        
        Returns:
            Dict con 'success' y 'message'
        """
        postulacion = self.postulacion_repo.get_by_id(postulacion_id)
        
        if not postulacion:
            return {'success': False, 'message': 'Postulación no encontrada'}
        
        # Validar que sea del trabajador
        if postulacion.id_trabajador.id_usuario != trabajador_id:
            return {'success': False, 'message': 'No tienes permisos para esta acción'}
        
        # Solo se puede retirar si está pendiente o en revisión
        if postulacion.estado not in ['pendiente', 'en_revision']:
            return {'success': False, 'message': 'No puedes retirar esta postulación'}
        
        # Eliminar
        if self.postulacion_repo.eliminar_postulacion(postulacion_id):
            return {'success': True, 'message': 'Postulación retirada correctamente'}
        
        return {'success': False, 'message': 'Error al retirar postulación'}
    
    def get_estadisticas_trabajador(self, trabajador_id: int) -> Dict:
        """
        Obtiene estadísticas de postulaciones de un trabajador
        
        Args:
            trabajador_id: ID del trabajador
        
        Returns:
            Dict con estadísticas
        """
        contadores = self.postulacion_repo.contar_postulaciones_trabajador(trabajador_id)
        
        # Calcular tasa de aceptación
        tasa_aceptacion = 0.0
        if contadores['total'] > 0:
            tasa_aceptacion = round(
                (contadores['aceptadas'] / contadores['total']) * 100,
                1
            )
        
        return {
            'total_postulaciones': contadores['total'],
            'postulaciones_pendientes': contadores['pendientes'],
            'postulaciones_aceptadas': contadores['aceptadas'],
            'postulaciones_rechazadas': contadores['rechazadas'],
            'tasa_aceptacion': tasa_aceptacion,
        }
    
    def _formatear_postulacion(self, postulacion) -> Dict:
        """Formatea una postulación para mostrar"""
        oferta = postulacion.oferta
        tipo = postulacion.tipo_oferta
        
        return {
            'id': postulacion.id_postulacion,
            'tipo': tipo,
            'titulo': oferta.titulo if tipo == 'usuario' else oferta.titulo_puesto,
            'descripcion': oferta.descripcion,
            'empleador': {
                'id': oferta.id_empleador.id_usuario,
                'nombre': oferta.id_empleador.nombre_completo,
            },
            'trabajador': {
                'id': postulacion.id_trabajador.id_usuario,
                'nombre': postulacion.id_trabajador.nombre_completo,
            },
            'mensaje': postulacion.mensaje,
            'pretension_salarial': postulacion.pretension_salarial,
            'disponibilidad_inmediata': postulacion.disponibilidad_inmediata,
            'estado': postulacion.estado,
            'estado_display': postulacion.get_estado_display(),
            'leida': postulacion.leida,
            'fecha_postulacion': postulacion.created_at,
            'oferta_id': oferta.id,
        }