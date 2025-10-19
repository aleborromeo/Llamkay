"""
Vistas de la app llamkay
"""
from .landing import home
from .about import nosotros
from .legal import terminos, privacidad
from .faq import preguntas_frecuentes
from .contact import contacto
from .dashboard import dashboard
from .settings import configuracion, ayuda, accesibilidad, comentarios

__all__ = [
    'home',
    'nosotros',
    'terminos',
    'privacidad',
    'preguntas_frecuentes',
    'contacto',
    'dashboard',
    'configuracion',
    'ayuda',
    'accesibilidad',
    'comentarios',
]