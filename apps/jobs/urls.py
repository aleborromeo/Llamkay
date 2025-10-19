from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    # Listado y búsqueda de trabajos
    path('', views.all_trabajos, name='all_trabajos'),
    path('filtrar/', views.filtrar_trabajos, name='filtrar_trabajos'),
    
    # Registro de ofertas
    path('registro-individual/', views.registro_individual, name='registro_individual'),
    path('registro-empresa/', views.registro_empresa, name='registro_empresa'),
    
    # Administración de trabajos del empleador
    path('mis-trabajos/', views.mis_trabajos, name='mis_trabajos'),
    path('mis-trabajos/ajax/', views.mis_trabajos_ajax, name='mis_trabajos_ajax'),
    path('editar/<int:oferta_id>/', views.editar_trabajo, name='editar_oferta'),
    path('eliminar/<int:oferta_id>/', views.eliminar_trabajo, name='eliminar_oferta'),
    
    # Dashboard de trabajador (buscar trabajo)
    path('dashboard-trabajador/', views.dashboard_trabajador, name='dashboard_trabajador'),
    path('guardar/<str:tipo_oferta>/<int:oferta_id>/', views.guardar_trabajo, name='guardar_trabajo'),
    path('trabajos-guardados/', views.trabajos_guardados, name='trabajos_guardados'),
    path('trabajos-guardados-ajax/', views.trabajos_guardados_ajax, name='trabajos_guardados_ajax'),
    path('quitar-guardado/<int:id>/', views.quitar_guardado, name='quitar_guardado'),
    
    # AJAX para ubicación
    path('ajax/cargar-provincias/', views.cargar_provincias, name='ajax_cargar_provincias'),
    path('ajax/cargar-distritos/', views.cargar_distritos, name='ajax_cargar_distritos'),
    path('ajax/cargar-comunidades/', views.cargar_comunidades, name='ajax_cargar_comunidades'),
]