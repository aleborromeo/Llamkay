"""
URLs del módulo Jobs - CORREGIDAS Y ORGANIZADAS
"""
from django.urls import path
from .views import (
    busqueda,
    ofertas,
    postulaciones,
    guardados,
    dashboard,
)

app_name = 'jobs'

urlpatterns = [
    # ==================== BÚSQUEDA Y LISTADO ====================
    path('', busqueda.all_trabajos, name='all_trabajos'),
    path('buscar/', busqueda.buscar_trabajos, name='buscar_trabajos'),
    path('filtrar/', busqueda.filtrar_trabajos, name='filtrar_trabajos'),
    path('detalle/<str:tipo>/<int:trabajo_id>/', busqueda.detalle_trabajo, name='detalle_trabajo'),
    
    # ==================== GESTIÓN DE OFERTAS ====================
    # Registro
    path('registro-individual/', ofertas.registro_individual, name='registro_individual'),
    path('registro-empresa/', ofertas.registro_empresa, name='registro_empresa'),
    
    # Administración
    path('mis-trabajos/', ofertas.mis_trabajos, name='mis_trabajos'),
    path('mis-trabajos/ajax/', ofertas.mis_trabajos_ajax, name='mis_trabajos_ajax'),
    path('editar/<int:oferta_id>/', ofertas.editar_trabajo, name='editar_oferta'),
    path('eliminar/<int:oferta_id>/', ofertas.eliminar_trabajo, name='eliminar_oferta'),
    path('cambiar-estado/<int:oferta_id>/', ofertas.cambiar_estado_oferta, name='cambiar_estado_oferta'),
    
    # ==================== DASHBOARDS ====================
    path('dashboard-trabajador/', dashboard.dashboard_trabajador, name='dashboard_trabajador'),
    path('dashboard-empleador/', dashboard.dashboard_empleador, name='dashboard_empleador'),
    path('admin-empleador/', dashboard.admin_empleador, name='admin_empleador'),
    path('admin-empresa/', dashboard.admin_empresa, name='admin_empresa'),
    
    # ==================== TRABAJOS GUARDADOS ====================
    path('guardar/<str:tipo>/<int:oferta_id>/', guardados.guardar_trabajo, name='guardar_trabajo'),
    path('trabajos-guardados/', guardados.trabajos_guardados, name='trabajos_guardados'),
    path('trabajos-guardados/ajax/', guardados.trabajos_guardados_ajax, name='trabajos_guardados_ajax'),
    path('quitar-guardado/<int:guardado_id>/', guardados.quitar_guardado, name='quitar_guardado'),
    
    # ==================== POSTULACIONES ====================
    # Trabajador
    path('postular/<str:tipo>/<int:oferta_id>/', postulaciones.postular_trabajo, name='postular_trabajo'),
    path('mis-postulaciones/', postulaciones.mis_postulaciones, name='mis_postulaciones'),
    path('retirar-postulacion/<int:postulacion_id>/', postulaciones.retirar_postulacion, name='retirar_postulacion'),
    
    # Empleador
    path('ver-postulantes/<str:tipo>/<int:oferta_id>/', postulaciones.ver_postulantes, name='ver_postulantes'),
    path('aceptar-postulante/<int:postulacion_id>/', postulaciones.aceptar_postulante, name='aceptar_postulante'),
    path('rechazar-postulante/<int:postulacion_id>/', postulaciones.rechazar_postulante, name='rechazar_postulante'),
    
    # ==================== AJAX UBICACIÓN ====================
    path('ajax/cargar-provincias/', ofertas.cargar_provincias, name='ajax_cargar_provincias'),
    path('ajax/cargar-distritos/', ofertas.cargar_distritos, name='ajax_cargar_distritos'),
    path('ajax/cargar-comunidades/', ofertas.cargar_comunidades, name='ajax_cargar_comunidades'),
]