"""
Views del módulo Jobs
"""
from .busqueda_views import busqueda_views
from .postulacion_views import postulacion_views
from .guardado_views import guardado_views
from .dashboard_views import dashboard_views

__all__ = [
    'busqueda_views',
    'postulacion_views',
    'guardado_views',
    'dashboard_views',
]