"""
URLs del módulo Jobs - Refactorizado
Rutas solo para trabajadores
"""
from django.urls import path
from apps.jobs.views import busqueda_views, postulacion_views, guardado_views, dashboard_views, ajax_views

app_name = 'jobs'

urlpatterns = [
    # ==================== BÚSQUEDA Y LISTADO ====================
    path('', busqueda_views.all_trabajos, name='all_trabajos'),
    path('buscar/', busqueda_views.buscar_trabajos, name='buscar_trabajos'),
    path('filtrar/', busqueda_views.filtrar_trabajos, name='filtrar_trabajos'),
    path('detalle/<str:tipo>/<int:trabajo_id>/', busqueda_views.detalle_trabajo, name='detalle_trabajo'),
    
    # ==================== DASHBOARD TRABAJADOR ====================
    path('dashboard-trabajador/', dashboard_views.dashboard_trabajador, name='dashboard_trabajador'),
    
    # ==================== TRABAJOS GUARDADOS ====================
    path('guardar/<str:tipo>/<int:oferta_id>/', guardado_views.guardar_trabajo, name='guardar_trabajo'),
    path('trabajos-guardados/', guardado_views.trabajos_guardados, name='trabajos_guardados'),
    path('trabajos-guardados/ajax/', guardado_views.trabajos_guardados_ajax, name='trabajos_guardados_ajax'),
    path('quitar-guardado/<int:guardado_id>/', guardado_views.quitar_guardado, name='quitar_guardado'),
    
    # ==================== POSTULACIONES ====================
    path('postular/<str:tipo>/<int:oferta_id>/', postulacion_views.postular_trabajo, name='postular_trabajo'),
    path('mis-postulaciones/', postulacion_views.mis_postulaciones, name='mis_postulaciones'),
    path('retirar-postulacion/<int:postulacion_id>/', postulacion_views.retirar_postulacion, name='retirar_postulacion'),
    
    path('ajax/cargar-provincias/', ajax_views.cargar_provincias, name='ajax_cargar_provincias'),
    path('ajax/cargar-distritos/', ajax_views.cargar_distritos, name='ajax_cargar_distritos'),
]