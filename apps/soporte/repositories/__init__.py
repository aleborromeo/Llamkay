"""
Repositorios de Soporte
Capa de acceso a datos
"""
from .denuncia_repository import DenunciaRepository
from .notificacion_repository import NotificacionRepository

__all__ = [
    'DenunciaRepository',
    'NotificacionRepository',
]