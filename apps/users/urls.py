"""
URLs de la aplicación de usuarios
"""

from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Autenticación
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Registro 
    path('seleccionar-tipo/', views.seleccionar_tipo, name='seleccionar_tipo'),
    path('register/step-2/', views.register_two, name='register_two'),
    path('register/step-3/', views.register_three, name='register_three'),
    path('register/step-4/', views.register_four, name='register_four'),
    path('register/', views.register, name='register'), 
    
    # APIs
    path('api/consultar-dni/', views.consultar_dni_api, name='consultar_dni_api'),
    path('api/consultar-ruc/', views.consultar_ruc_api, name='consultar_ruc_api'),
    path('validar-correo/', views.validar_correo, name='validar_correo'),
    path('cargar-provincias/', views.cargar_provincias, name='cargar_provincias'),
    path('cargar-distritos/', views.cargar_distritos, name='cargar_distritos'),
    
    # Perfil
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/actualizar/', views.actualizar_perfil, name='actualizar_perfil'),
    path('perfil/exportar/', views.exportar_portafolio_pdf, name='exportar_portafolio'),
    
    # Calificaciones
    path('calificar/<int:usuario_id>/', views.calificar_usuario, name='calificar_usuario'),
    path('buscar/', views.buscar_usuarios, name='buscar_usuarios'),
]