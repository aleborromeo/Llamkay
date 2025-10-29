from django.urls import path
from apps.empleadores.views import oferta_views, postulante_views, dashboard_views

app_name = 'empleadores'

urlpatterns = [
    path('dashboard/', dashboard_views.dashboard_empleador, name='dashboard'),
    
    path('ofertas/individual/crear/', oferta_views.registro_individual, name='crear_oferta_individual'),
    path('ofertas/empresa/crear/', oferta_views.registro_empresa, name='crear_oferta_empresa'),
    path('ofertas/mis-trabajos/', oferta_views.mis_trabajos, name='mis_trabajos'),
    path('ofertas/mis-trabajos/ajax/', oferta_views.mis_trabajos_ajax, name='mis_trabajos_ajax'),
    path('ofertas/editar/<int:oferta_id>/', oferta_views.editar_trabajo, name='editar_trabajo'),
    path('ofertas/eliminar/<int:oferta_id>/', oferta_views.eliminar_trabajo, name='eliminar_trabajo'),
    path('ofertas/cambiar-estado/<int:oferta_id>/', oferta_views.cambiar_estado_oferta, name='cambiar_estado_oferta'),
    
    path('postulantes/<str:tipo>/<int:oferta_id>/', postulante_views.ver_postulantes, name='ver_postulantes'),
    path('postulantes/aceptar/<int:postulacion_id>/', postulante_views.aceptar_postulante, name='aceptar_postulante'),
    path('postulantes/rechazar/<int:postulacion_id>/', postulante_views.rechazar_postulante, name='rechazar_postulante'),
    path('postulantes/recientes/', postulante_views.postulaciones_recientes, name='postulaciones_recientes'),
    
    path('ajax/cargar-provincias/', oferta_views.cargar_provincias, name='cargar_provincias'),
    path('ajax/cargar-distritos/', oferta_views.cargar_distritos, name='cargar_distritos'),
    path('ajax/cargar-comunidades/', oferta_views.cargar_comunidades, name='cargar_comunidades'),
]