"""
Modelos del módulo Users
Divididos por responsabilidad siguiendo SRP
"""

from .ubicacion import Departamento, Provincia, Distrito, Comunidad
from .usuario import Usuario
from .profile import Profile, UsuarioEstadisticas
from .habilidad import Habilidad, UsuarioHabilidad, CategoriaTrabajo, UsuarioCategoria
from .verificacion import Verificacion, Certificacion, TrabajosRealizados
from .disponibilidad import Disponibilidad

__all__ = [
    # Ubicación
    'Departamento',
    'Provincia',
    'Distrito',
    'Comunidad',
    
    # Usuario
    'Usuario',
    'Profile',
    'UsuarioEstadisticas',
    
    # Habilidades
    'Habilidad',
    'UsuarioHabilidad',
    'CategoriaTrabajo',
    'UsuarioCategoria',
    
    # Verificación
    'Verificacion',
    'Certificacion',
    'TrabajosRealizados',
    
    # Disponibilidad
    'Disponibilidad',
]