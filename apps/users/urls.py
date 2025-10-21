"""
URLs de la aplicación de usuarios
"""

from django.urls import path
from .views import api, auth, calificacion, perfil, verificacion

app_name = 'users'

urlpatterns = [
    # Autenticación
    path('login/', auth.login, name='login'),
    path('logout/', auth.logout_view, name='logout'),
    
    # Registro 
    path('seleccionar-tipo/', auth.seleccionar_tipo, name='seleccionar_tipo'),
    path('register/step-2/', auth.register_two, name='register_two'),
    path('register/step-3/', auth.register_three, name='register_three'),
    path('register/step-4/', auth.register_four, name='register_four'),
    path('register/', auth.register, name='register'), 
    
    # APIs
    path('api/consultar-dni/', api.consultar_dni_api, name='consultar_dni_api'),
    path('api/consultar-ruc/', api.consultar_ruc_api, name='consultar_ruc_api'),
    path('validar-correo/', auth.validar_correo, name='validar_correo'),
    path('cargar-provincias/', api.cargar_provincias, name='cargar_provincias'),
    path('cargar-distritos/', api.cargar_distritos, name='cargar_distritos'),
    
    # Perfil
    path('perfil/', perfil.perfil, name='perfil'),
    path('perfil/actualizar/', perfil.actualizar_perfil, name='actualizar_perfil'),
    path('perfil/exportar/', perfil.exportar_portafolio_pdf, name='exportar_portafolio'),
    
    # Calificaciones
    path('calificar/<int:usuario_id>/', calificacion.calificar_usuario, name='calificar_usuario'),
    path('buscar/', calificacion.buscar_usuarios, name='buscar_usuarios'),
]