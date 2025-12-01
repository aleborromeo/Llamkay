"""
Repository de Notificaciones
SRP: Solo maneja el acceso a datos de notificaciones
"""
from django.db.models import QuerySet
from typing import Optional, List
import logging

from ..models import Notificacion
from apps.users.models import Usuario

logger = logging.getLogger(__name__)


class NotificacionRepository:
    """
    Repository para operaciones CRUD de Notificaciones
    """
    
    @staticmethod
    def crear(id_usuario: Usuario, tipo: str, titulo: str, 
              mensaje: str = "", url: str = "") -> Optional[Notificacion]:
        """
        Crea una nueva notificación
        """
        try:
            notificacion = Notificacion.objects.create(
                id_usuario=id_usuario,
                tipo=tipo,
                titulo=titulo,
                mensaje=mensaje,
                url=url,
                leida=False
            )
            logger.info(f"Notificación creada: {notificacion.id_notificacion}")
            return notificacion
        except Exception as e:
            logger.error(f"Error creando notificación: {str(e)}")
            return None
    
    @staticmethod
    def obtener_por_id(id_notificacion: int) -> Optional[Notificacion]:
        """
        Obtiene una notificación por ID
        """
        try:
            return Notificacion.objects.get(id_notificacion=id_notificacion)
        except Notificacion.DoesNotExist:
            return None
    
    @staticmethod
    def obtener_por_usuario(id_usuario: Usuario) -> QuerySet:
        """
        Obtiene todas las notificaciones de un usuario
        """
        return Notificacion.objects.filter(
            id_usuario=id_usuario
        ).order_by('-created_at')
    
    @staticmethod
    def obtener_no_leidas(id_usuario: Usuario) -> QuerySet:
        """
        Obtiene notificaciones no leídas de un usuario
        """
        return Notificacion.objects.filter(
            id_usuario=id_usuario,
            leida=False
        ).order_by('-created_at')
    
    @staticmethod
    def contar_no_leidas(id_usuario: Usuario) -> int:
        """
        Cuenta las notificaciones no leídas
        """
        return Notificacion.objects.filter(
            id_usuario=id_usuario,
            leida=False
        ).count()
    
    @staticmethod
    def marcar_como_leida(id_notificacion: int) -> bool:
        """
        Marca una notificación como leída
        """
        try:
            notificacion = Notificacion.objects.get(id_notificacion=id_notificacion)
            notificacion.leida = True
            notificacion.save()
            return True
        except Notificacion.DoesNotExist:
            return False
    
    @staticmethod
    def marcar_todas_leidas(id_usuario: Usuario) -> int:
        """
        Marca todas las notificaciones de un usuario como leídas
        Retorna el número de notificaciones actualizadas
        """
        return Notificacion.objects.filter(
            id_usuario=id_usuario,
            leida=False
        ).update(leida=True)
    
    @staticmethod
    def eliminar(id_notificacion: int) -> bool:
        """
        Elimina una notificación
        """
        try:
            notificacion = Notificacion.objects.get(id_notificacion=id_notificacion)
            notificacion.delete()
            return True
        except Notificacion.DoesNotExist:
            return False