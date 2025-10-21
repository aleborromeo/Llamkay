"""
Inicialización del paquete views
Importa todos los módulos de vistas para facilitar el acceso
"""

from . import api
from . import auth
from . import calificacion
from . import perfil
from . import verificacion

__all__ = [
    'api',
    'auth', 
    'calificacion',
    'perfil',
    'verificacion',
]