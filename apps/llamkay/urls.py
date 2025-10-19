"""
URLs de la app llamkay (landing pages y páginas estáticas)
"""
from django.urls import path
from .views import (
    home,
    nosotros,
    terminos,
    privacidad,
    preguntas_frecuentes,
    contacto,
    dashboard,
    configuracion,
    ayuda,
    accesibilidad,
    comentarios,
)

app_name = 'llamkay'

urlpatterns = [
    # Landing page
    path('', home, name='index'),
    path('home/', home, name='home'),
    
    # Dashboard
    path('dashboard/', dashboard, name='dashboard'),
    
    # Páginas informativas
    path('nosotros/', nosotros, name='nosotros'),
    path('contacto/', contacto, name='contacto'),
    path('faq/', preguntas_frecuentes, name='faq'),
    path('preguntas-frecuentes/', preguntas_frecuentes, name='preguntas_frecuentes'),
    
    # Páginas legales
    path('terminos/', terminos, name='terminos'),
    path('privacidad/', privacidad, name='privacidad'),
    
    # Páginas de configuración (settings)
    path('configuracion/', configuracion, name='configuracion'),
    path('ayuda/', ayuda, name='ayuda'),
    path('accesibilidad/', accesibilidad, name='accesibilidad'),
    path('comentarios/', comentarios, name='comentarios'),
]