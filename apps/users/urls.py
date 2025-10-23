"""
URLs de la aplicación de usuarios - REFACTORIZADAS
Importa desde los nuevos módulos de vistas
"""

from django.urls import path
from .views import api_views, auth_views, calificacion_views, perfil_views, verificacion_views

app_name = 'users'

urlpatterns = [
    # ==================== AUTENTICACIÓN ====================
    path('login/', auth_views.login, name='login'),
    path('logout/', auth_views.logout_view, name='logout'),
    
    # Registro 
    path('seleccionar-tipo/', auth_views.seleccionar_tipo, name='seleccionar_tipo'),
    path('register/', auth_views.register, name='register'),
    path('register/step-2/', auth_views.register_two, name='register_two'),
    path('register/step-3/', auth_views.register_three, name='register_three'),
    path('register/step-4/', auth_views.register_four, name='register_four'),
    
    # Validación
    path('validar-correo/', auth_views.validar_correo, name='validar_correo'),
    
    # ==================== APIs DE CONSULTA ====================
    path('api/consultar-dni/', api_views.consultar_dni_api, name='consultar_dni_api'),
    path('api/consultar-ruc/', api_views.consultar_ruc_api, name='consultar_ruc_api'),
    path('cargar-provincias/', api_views.cargar_provincias, name='cargar_provincias'),
    path('cargar-distritos/', api_views.cargar_distritos, name='cargar_distritos'),
    path('cargar-comunidades/', api_views.cargar_comunidades, name='cargar_comunidades'),
    
    # ==================== PERFIL PERSONAL ====================
    path('perfil/', perfil_views.perfil, name='perfil'),
    path('perfil/actualizar/', perfil_views.actualizar_perfil, name='actualizar_perfil'),
    path('perfil/exportar/', perfil_views.exportar_portafolio_pdf, name='exportar_portafolio'),
    
    # ==================== PERFIL PÚBLICO ====================
    path('perfil/<int:usuario_id>/', perfil_views.perfil_publico, name='perfil_publico'),
    
    # ==================== BÚSQUEDA ====================
    path('buscar/', calificacion_views.buscar_usuarios, name='buscar_usuarios'),
    
    # ==================== CALIFICACIONES ====================
    path('calificar/<int:usuario_id>/', calificacion_views.calificar_usuario, name='calificar_usuario'),
    path('calificaciones/<int:usuario_id>/', calificacion_views.ver_calificaciones, name='ver_calificaciones'),
    path('mis-calificaciones/', calificacion_views.mis_calificaciones, name='mis_calificaciones'),
    path('calificacion/<int:calificacion_id>/eliminar/', calificacion_views.eliminar_calificacion, name='eliminar_calificacion'),
    
    # ==================== VERIFICACIÓN ====================
    path('verificacion/solicitar/', verificacion_views.solicitar_verificacion, name='solicitar_verificacion'),
    path('verificacion/mis-verificaciones/', verificacion_views.mis_verificaciones, name='mis_verificaciones'),
    path('certificacion/subir/', verificacion_views.subir_certificacion, name='subir_certificacion'),
    path('certificacion/mis-certificaciones/', verificacion_views.mis_certificaciones, name='mis_certificaciones'),
]