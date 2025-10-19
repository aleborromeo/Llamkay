"""
Vistas de Configuración y Páginas de Settings
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)


@login_required
def configuracion(request):
    """
    Página de Configuración y Privacidad
    """
    logger.info(f"⚙️ Usuario {request.user.username} accedió a Configuración")
    print(f"✅ CONFIGURACIÓN cargada para: {request.user.username}")
    
    context = {
        'page_title': 'Configuración y Privacidad',
        'page_content': 'Aquí podrás gestionar tu configuración de cuenta, privacidad y preferencias.',
        'user': request.user,
    }
    return render(request, 'llamkay/settings/configuracion.html', context)


@login_required
def ayuda(request):
    """
    Página de Ayuda y Soporte Técnico
    """
    logger.info(f"❓ Usuario {request.user.username} accedió a Ayuda")
    print(f"✅ AYUDA cargada para: {request.user.username}")
    
    context = {
        'page_title': 'Ayuda y Soporte Técnico',
        'page_content': 'Centro de ayuda con preguntas frecuentes, tutoriales y soporte.',
        'user': request.user,
    }
    return render(request, 'llamkay/settings/ayuda.html', context)


@login_required
def accesibilidad(request):
    """
    Página de Pantalla y Accesibilidad
    """
    logger.info(f"♿ Usuario {request.user.username} accedió a Accesibilidad")
    print(f"✅ ACCESIBILIDAD cargada para: {request.user.username}")
    
    context = {
        'page_title': 'Pantalla y Accesibilidad',
        'page_content': 'Opciones de accesibilidad, tamaño de texto, contraste y más.',
        'user': request.user,
    }
    return render(request, 'llamkay/settings/accesibilidad.html', context)


@login_required
def comentarios(request):
    """
    Página de Enviar Comentarios
    """
    logger.info(f"💬 Usuario {request.user.username} accedió a Comentarios")
    print(f"✅ COMENTARIOS cargada para: {request.user.username}")
    
    context = {
        'page_title': 'Enviar Comentarios',
        'page_content': 'Envíanos tus sugerencias, reportes de bugs o comentarios sobre la plataforma.',
        'user': request.user,
    }
    return render(request, 'llamkay/settings/comentarios.html', context)