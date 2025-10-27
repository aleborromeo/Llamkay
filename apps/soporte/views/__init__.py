"""
Vistas de Soporte
"""
from .notificacion_views import (
    listar_notificaciones,
    marcar_notificacion_leida,
    marcar_todas_leidas,
    eliminar_notificacion,
)

from .denuncia_views import (
    crear_denuncia,
    listar_denuncias,
    detalle_denuncia,
)

__all__ = [
    # Notificaciones
    'listar_notificaciones',
    'marcar_notificacion_leida',
    'marcar_todas_leidas',
    'eliminar_notificacion',
    
    # Denuncias
    'crear_denuncia',
    'listar_denuncias',
    'detalle_denuncia',
]