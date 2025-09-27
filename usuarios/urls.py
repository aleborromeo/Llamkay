from django.urls import path
from . import views, utils

app_name = 'usuarios'

urlpatterns = [
    # Autenticación
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('validar_correo/', views.validar_correo, name='validar_correo'),

    # Registro multi-paso
    path('register/', views.register, name='register'),
    path('register/<str:tipo_usuario>/', views.register, name='register_tipo'),
    path('seleccionar_tipo/', views.seleccionar_tipo, name='seleccionar_tipo'),
    path('ubicacion/', views.register_two, name='register_two'),
    path('habilidades/', views.register_three, name='register_three'),
    path('antecedentes/', views.register_four, name='register_four'),

    # Perfil
    path('perfil/', views.perfil, name='perfil'),
    path('actualizar_perfil/', views.actualizar_perfil, name='actualizar_perfil'),

    # Dashboard y configuración
    path('dashboard/', views.dashboard, name='dashboard'),
    path('configuracion/', views.configuracion, name='configuracion'),
    path('ayuda/', views.ayuda, name='ayuda'),
    path('accesibilidad/', views.accesibilidad, name='accesibilidad'),
    path('comentarios/', views.comentarios, name='comentarios'),

    # Ubicación dinámica
    path('cargar_provincias/', utils.cargar_provincias, name='cargar_provincias'),
    path('cargar_distritos/', utils.cargar_distritos, name='cargar_distritos'),

    # Consultas externas
    path('buscar-dni/', utils.buscar_dni, name='buscar_dni'),
    path('buscar-ruc/', utils.buscar_ruc, name='buscar_ruc'),
    
    #AJAX
    path('subir_certificaciones/', utils.subir_certificaciones, name='subir_certificaciones'),
    
    #Exportar Portafolio
    path('exportar-portafolio/', views.exportar_portafolio_pdf, name='exportar_portafolio_pdf'),
    
    path('buscar/', views.buscar_usuarios,   name='buscar_usuarios'),
    path('calificar/<int:usuario_id>/', views.calificar_usuario, name='calificar'),
]