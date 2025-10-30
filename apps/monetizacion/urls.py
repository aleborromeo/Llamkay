"""
URLs del módulo de Monetización
"""
from django.urls import path
from .views.pago_views import (
    planes_list,
    plan_detail,
    elegir_metodo_pago,
    crear_pago_gratis,
    procesar_pago_yape_plin,
    verificar_pago,
    confirmar_pago_manual,
    pago_exitoso,
    pago_cancelado,
    suscripcion_detalle,
    suscripcion_exitosa,
)

app_name = 'monetizacion'

urlpatterns = [
    # ==================== PLANES ====================
    path('planes/', planes_list, name='planes_list'),
    path('planes/<int:plan_id>/', plan_detail, name='plan_detail'),

    # ==================== PAGOS ====================
    path('planes/<int:plan_id>/pago/', elegir_metodo_pago, name='elegir_metodo_pago'),
    path('pago/gratis/<int:plan_id>/', crear_pago_gratis, name='crear_pago_gratis'),
    path('pago/<int:plan_id>/procesar/', procesar_pago_yape_plin, name='procesar_pago_yape_plin'),
    path('pago/<int:payment_id>/verificar/', verificar_pago, name='verificar_pago'),
    path('pago/<int:payment_id>/confirmar/', confirmar_pago_manual, name='confirmar_pago_manual'),
    path('pago/exitoso/', pago_exitoso, name='pago_exitoso'),
    path('pago/cancelado/', pago_cancelado, name='pago_cancelado'),

    # ==================== SUSCRIPCIÓN ====================
    path('suscripcion/', suscripcion_detalle, name='suscripcion_detalle'),
    path('suscripcion/exitosa/', suscripcion_exitosa, name='suscripcion_exitosa'),
]
