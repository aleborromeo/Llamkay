from django.urls import path
from . import views
from usuarios.decoradores import rol_requerido
from django.shortcuts import render

app_name = 'trabajos'

def test_css_view(request):
    return render(request, 'trabajos/test_css.html')

urlpatterns = [
    # Test CSS
    path('test-css/', test_css_view, name='test_css'),
    
    path('all-trabajos/', views.all_trabajos, name='all_trabajos'),

    # Para usuarios que ofrecen trabajo o ambos
    path('registro-individual/', rol_requerido(['ofrecer-trabajo', 'ambos'])(views.registro_individual), name='registro_individual'),

    # Para empresas exclusivamente
    path('registro-empresa/', rol_requerido(['empresa'])(views.registro_empresa), name='registro_empresa'),

    # Administración de trabajos -- empleador
    path('mis_trabajos/', rol_requerido(['ofrecer-trabajo', 'ambos','empresa'])(views.mis_trabajos), name='mis_trabajos'),

    path('mis-trabajos/ajax/', rol_requerido(['ofrecer-trabajo', 'ambos','empresa'])(views.mis_trabajos_ajax), name='mis_trabajos_ajax'),

    path('admin-empleador/', rol_requerido(['ofrecer-trabajo', 'ambos'])(views.admin_empleador), name='admin_empleador'),

    path('editar-oferta/<int:oferta_id>/', rol_requerido(['ofrecer-trabajo', 'ambos','empresa'])(views.editar_trabajo), name='editar_oferta'),



    path('eliminar-oferta/<int:oferta_id>/', rol_requerido(['ofrecer-trabajo', 'ambos'])(views.eliminar_trabajo), name='eliminar_oferta'),

    # Administración de trabajos -- empresa
    path('admin-empresa/', rol_requerido(['empresa'])(views.admin_empresa), name='admin_empresa'),

    # Filtrado de trabajos
    path('filtrar-trabajos/', views.filtrar_trabajos, name='filtrar_trabajos'),

    # Detalle de trabajos y AJAX
    path('ajax/cargar-provincias/', views.cargar_provincias, name='ajax_cargar_provincias'),
    path('ajax/cargar-distritos/', views.cargar_distritos, name='ajax_cargar_distritos'),
    path('ajax/cargar-comunidades/', views.cargar_comunidades, name='ajax_cargar_comunidades'),
    
    
    
    # Dashboard de trabajador
    path('dashboard-trabajador/', rol_requerido(['buscar-trabajo'])(views.dashboard_trabajador), name='dashboard_trabajador'),
    
    path('guardar/<str:tipo_oferta>/<int:oferta_id>/', views.guardar_trabajo, name='guardar_trabajo'),

    path('trabajos-guardados/', rol_requerido(['buscar-trabajo'])(views.trabajos_guardados), name='trabajos_guardados'),
    path('trabajos-guardados-ajax/', views.trabajos_guardados_ajax, name='trabajos_guardados_ajax'),

    
    
    
    # urls.py
    path('quitar-guardado/<int:id>/', views.quitar_guardado, name='quitar_guardado')

]

