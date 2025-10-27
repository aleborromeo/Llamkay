"""
Servicio de Notificaciones
SRP: Solo maneja lógica de negocio de notificaciones
OCP: Extendible agregando nuevos tipos de notificaciones
DIP: Depende de NotificacionRepository (abstracción)
"""
from typing import Optional, Dict, Any
from django.utils import timezone
import logging

from ..repositories import NotificacionRepository

logger = logging.getLogger(__name__)


class NotificacionService:
    """
    Servicio para gestionar notificaciones
    SRP: Una sola responsabilidad - lógica de notificaciones
    """
    
    def __init__(self):
        self.repo = NotificacionRepository()
    
    def crear_notificacion(
        self,
        id_usuario,
        tipo: str,
        titulo: str,
        mensaje: Optional[str] = None,
        entity_tipo: Optional[str] = None,
        entity_id: Optional[int] = None,
        url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Crear una nueva notificación
        
        Args:
            id_usuario: Usuario que recibirá la notificación
            tipo: Tipo de notificación (postulacion, mensaje, contrato, etc.)
            titulo: Título de la notificación
            mensaje: Contenido de la notificación
            entity_tipo: Tipo de entidad relacionada
            entity_id: ID de la entidad relacionada
            url: URL para redireccionar
        """
        try:
            data = {
                'id_usuario': id_usuario,
                'tipo': tipo,
                'titulo': titulo,
                'mensaje': mensaje,
                'entity_tipo': entity_tipo,
                'entity_id': entity_id,
                'url': url,
            }
            
            notificacion = self.repo.create(data)
            
            logger.info(
                f"✅ Notificación creada: {tipo} para usuario {id_usuario.id_usuario}"
            )
            
            return {
                'success': True,
                'notificacion': notificacion,
                'message': 'Notificación creada exitosamente'
            }
            
        except Exception as e:
            logger.error(f"❌ Error creando notificación: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    # ==================== NOTIFICACIONES POR TIPO ====================
    
    def notificar_nueva_postulacion(self, empleador, trabajador, oferta_titulo: str, postulacion_id: int):
        """Notificar al empleador sobre una nueva postulación"""
        return self.crear_notificacion(
            id_usuario=empleador,
            tipo='postulacion',
            titulo='Nueva postulación recibida',
            mensaje=f'{trabajador.nombres} {trabajador.apellidos} ha postulado a "{oferta_titulo}"',
            entity_tipo='postulacion',
            entity_id=postulacion_id,
            url=f'/postulaciones/{postulacion_id}/'
        )
    
    def notificar_postulacion_aceptada(self, trabajador, empleador, oferta_titulo: str, contrato_id: int):
        """Notificar al trabajador que su postulación fue aceptada"""
        return self.crear_notificacion(
            id_usuario=trabajador,
            tipo='postulacion',
            titulo='¡Tu postulación fue aceptada!',
            mensaje=f'{empleador.nombres} {empleador.apellidos} aceptó tu postulación para "{oferta_titulo}"',
            entity_tipo='contrato',
            entity_id=contrato_id,
            url=f'/contratos/{contrato_id}/'
        )
    
    def notificar_postulacion_rechazada(self, trabajador, empleador, oferta_titulo: str):
        """Notificar al trabajador que su postulación fue rechazada"""
        return self.crear_notificacion(
            id_usuario=trabajador,
            tipo='postulacion',
            titulo='Postulación no aceptada',
            mensaje=f'Tu postulación para "{oferta_titulo}" no fue seleccionada en esta ocasión',
            entity_tipo='postulacion',
            entity_id=None,
            url='/trabajos/'
        )
    
    def notificar_nuevo_mensaje(self, receptor, remitente, conversacion_id: int):
        """Notificar sobre un nuevo mensaje"""
        return self.crear_notificacion(
            id_usuario=receptor,
            tipo='mensaje',
            titulo='Nuevo mensaje',
            mensaje=f'{remitente.nombres} {remitente.apellidos} te ha enviado un mensaje',
            entity_tipo='conversacion',
            entity_id=conversacion_id,
            url=f'/chat/{conversacion_id}/'
        )
    
    def notificar_contrato_creado(self, trabajador, empleador, contrato_id: int):
        """Notificar creación de contrato"""
        return self.crear_notificacion(
            id_usuario=trabajador,
            tipo='contrato',
            titulo='Nuevo contrato creado',
            mensaje=f'{empleador.nombres} {empleador.apellidos} ha creado un contrato contigo',
            entity_tipo='contrato',
            entity_id=contrato_id,
            url=f'/contratos/{contrato_id}/'
        )
    
    def notificar_contrato_completado(self, empleador, trabajador, contrato_id: int):
        """Notificar finalización de contrato"""
        return self.crear_notificacion(
            id_usuario=empleador,
            tipo='contrato',
            titulo='Trabajo completado',
            mensaje=f'{trabajador.nombres} {trabajador.apellidos} ha marcado el trabajo como completado',
            entity_tipo='contrato',
            entity_id=contrato_id,
            url=f'/contratos/{contrato_id}/'
        )
    
    def notificar_pago_recibido(self, trabajador, monto: float, contrato_id: int):
        """Notificar pago recibido"""
        return self.crear_notificacion(
            id_usuario=trabajador,
            tipo='pago',
            titulo='Pago recibido',
            mensaje=f'Has recibido un pago de S/. {monto:.2f}',
            entity_tipo='contrato',
            entity_id=contrato_id,
            url=f'/contratos/{contrato_id}/'
        )
    
    def notificar_nueva_calificacion(self, receptor, autor, puntuacion: int, contrato_id: int):
        """Notificar nueva calificación"""
        estrellas = '⭐' * puntuacion
        return self.crear_notificacion(
            id_usuario=receptor,
            tipo='calificacion',
            titulo='Nueva calificación recibida',
            mensaje=f'{autor.nombres} {autor.apellidos} te ha calificado: {estrellas}',
            entity_tipo='contrato',
            entity_id=contrato_id,
            url=f'/perfil/{receptor.id_usuario}/'
        )
    
    def notificar_verificacion_completada(self, usuario):
        """Notificar verificación completada"""
        return self.crear_notificacion(
            id_usuario=usuario,
            tipo='verificacion',
            titulo='¡Cuenta verificada!',
            mensaje='Tu cuenta ha sido verificada exitosamente. Ahora puedes acceder a más oportunidades',
            entity_tipo='usuario',
            entity_id=usuario.id_usuario,
            url='/perfil/'
        )
    
    def notificar_verificacion_rechazada(self, usuario, motivo: str):
        """Notificar verificación rechazada"""
        return self.crear_notificacion(
            id_usuario=usuario,
            tipo='verificacion',
            titulo='Verificación rechazada',
            mensaje=f'Tu verificación no pudo completarse: {motivo}. Por favor, intenta nuevamente',
            entity_tipo='usuario',
            entity_id=usuario.id_usuario,
            url='/verificacion/'
        )
    
    # ==================== GESTIÓN DE NOTIFICACIONES ====================
    
    def obtener_notificaciones(self, id_usuario, limit: int = 50):
        """Obtener notificaciones de un usuario"""
        try:
            return self.repo.get_by_usuario(id_usuario, limit)
        except Exception as e:
            logger.error(f"Error obteniendo notificaciones: {str(e)}")
            return []
    
    def obtener_no_leidas(self, id_usuario):
        """Obtener notificaciones no leídas"""
        try:
            return self.repo.get_no_leidas(id_usuario)
        except Exception as e:
            logger.error(f"Error obteniendo notificaciones no leídas: {str(e)}")
            return []
    
    def contar_no_leidas(self, id_usuario) -> int:
        """Contar notificaciones no leídas"""
        try:
            return self.repo.count_no_leidas(id_usuario)
        except Exception as e:
            logger.error(f"Error contando notificaciones: {str(e)}")
            return 0
    
    def marcar_leida(self, id_notificacion: int) -> bool:
        """Marcar notificación como leída"""
        try:
            return self.repo.marcar_como_leida(id_notificacion)
        except Exception as e:
            logger.error(f"Error marcando notificación como leída: {str(e)}")
            return False
    
    def marcar_todas_leidas(self, id_usuario) -> int:
        """Marcar todas las notificaciones como leídas"""
        try:
            count = self.repo.marcar_todas_leidas(id_usuario)
            logger.info(f"✅ {count} notificaciones marcadas como leídas")
            return count
        except Exception as e:
            logger.error(f"Error marcando todas como leídas: {str(e)}")
            return 0
    
    def eliminar_notificacion(self, id_notificacion: int) -> bool:
        """Eliminar una notificación"""
        try:
            return self.repo.delete_by_id(id_notificacion)
        except Exception as e:
            logger.error(f"Error eliminando notificación: {str(e)}")
            return False
    
    def limpiar_antiguas(self, dias: int = 30) -> int:
        """Limpiar notificaciones antiguas"""
        try:
            deleted = self.repo.delete_antiguas(dias)
            logger.info(f"✅ {deleted} notificaciones antiguas eliminadas")
            return deleted
        except Exception as e:
            logger.error(f"Error limpiando notificaciones: {str(e)}")
            return 0