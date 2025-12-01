"""
Repositories - Capa de Acceso a Datos
Implementan las interfaces definidas siguiendo DIP
"""

from .usuario_repository import UsuarioRepository
from .profile_repository import ProfileRepository
from .calificacion_repository import CalificacionRepository

__all__ = [
    'UsuarioRepository',
    'ProfileRepository',
    'CalificacionRepository',
]