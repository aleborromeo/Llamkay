"""
URLs del módulo de Soporte
"""
from django.urls import path
from .views import (
    # Notificaciones
    listar_notificaciones,
    marcar_notificacion_leida,
    marcar_todas_leidas,
    eliminar_notificacion,
    
    # Denuncias
    crear_denuncia,
    listar_denuncias,
    detalle_denuncia,
)

app_name = 'soporte'

urlpatterns = [
    # ==================== NOTIFICACIONES ====================
    path('notificaciones/', listar_notificaciones, name='notificaciones'),
    path('notificaciones/<int:id_notificacion>/leer/', marcar_notificacion_leida, name='marcar_leida'),
    path('notificaciones/marcar-todas-leidas/', marcar_todas_leidas, name='marcar_todas_leidas'),
    path('notificaciones/<int:id_notificacion>/eliminar/', eliminar_notificacion, name='eliminar_notificacion'),
    
    # ==================== DENUNCIAS ====================
    path('denuncias/', listar_denuncias, name='denuncias'),
    path('denuncias/crear/', crear_denuncia, name='crear_denuncia'),
    path('denuncias/<int:id_denuncia>/', detalle_denuncia, name='detalle_denuncia'),
]