"""
Vistas de Notificaciones
SRP: Solo maneja la presentación de notificaciones
DIP: Depende de NotificacionService (abstracción)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib import messages
from django.utils import timezone
import logging

from apps.soporte.services import NotificacionService
from apps.soporte.models import Notificacion

logger = logging.getLogger(__name__)


@login_required
def listar_notificaciones(request):
    """
    Vista para listar notificaciones del usuario
    GET: Muestra todas las notificaciones
    """
    try:
        service = NotificacionService()
        
        # Obtener el Usuario correcto
        from apps.users.models import Usuario
        try:
            usuario = Usuario.objects.get(user=request.user)
        except Usuario.DoesNotExist:
            messages.error(request, 'No se encontró tu perfil de usuario')
            return redirect('llamkay:dashboard')
        
        # Obtener notificaciones del usuario
        notificaciones = service.obtener_notificaciones_usuario(usuario)
        
        # Contar no leídas
        count_no_leidas = service.contar_no_leidas(usuario)
        
        context = {
            'notificaciones': notificaciones[:50],  # Últimas 50
            'count_no_leidas': count_no_leidas,
        }
        
        return render(request, 'soporte/notificaciones/lista.html', context)
        
    except Exception as e:
        logger.error(f"Error listando notificaciones: {str(e)}", exc_info=True)
        messages.error(request, 'Error al cargar las notificaciones')
        return redirect('llamkay:dashboard')


@login_required
@require_POST
def marcar_notificacion_leida(request, id_notificacion):
    """
    Marcar una notificación como leída
    POST: Marca como leída y devuelve JSON
    """
    try:
        from apps.users.models import Usuario
        usuario = Usuario.objects.get(user=request.user)
        
        service = NotificacionService()
        
        # Verificar que la notificación pertenece al usuario
        notificacion = get_object_or_404(
            Notificacion,
            id_notificacion=id_notificacion,
            id_usuario=usuario
        )
        
        # Marcar como leída
        result = service.marcar_como_leida(id_notificacion)
        
        if result['success']:
            return JsonResponse({
                'success': True,
                'message': 'Notificación marcada como leída'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': result.get('error', 'Error desconocido')
            }, status=400)
            
    except Exception as e:
        logger.error(f"Error marcando notificación como leída: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
@require_POST
def marcar_todas_leidas(request):
    """
    Marcar todas las notificaciones como leídas
    POST: Marca todas las notificaciones no leídas del usuario
    """
    try:
        from apps.users.models import Usuario
        usuario = Usuario.objects.get(user=request.user)
        
        service = NotificacionService()
        
        # Marcar todas como leídas
        result = service.marcar_todas_leidas(usuario)
        
        if result['success']:
            messages.success(request, result['message'])
        else:
            messages.error(request, result.get('error', 'Error al marcar notificaciones'))
        
        return redirect('soporte:notificaciones')
        
    except Exception as e:
        logger.error(f"Error marcando todas como leídas: {str(e)}")
        messages.error(request, 'Error al procesar la solicitud')
        return redirect('soporte:notificaciones')


@login_required
@require_POST
def eliminar_notificacion(request, id_notificacion):
    """
    Eliminar una notificación
    POST: Elimina la notificación y devuelve JSON
    """
    try:
        from apps.users.models import Usuario
        usuario = Usuario.objects.get(user=request.user)
        
        # Verificar que la notificación pertenece al usuario
        notificacion = get_object_or_404(
            Notificacion,
            id_notificacion=id_notificacion,
            id_usuario=usuario
        )
        
        # Eliminar
        notificacion.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Notificación eliminada'
        })
        
    except Exception as e:
        logger.error(f"Error eliminando notificación: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@login_required
def check_new_notifications(request):
    """
    Verificar si hay nuevas notificaciones (para polling)
    GET: Devuelve JSON con cantidad de notificaciones nuevas
    """
    try:
        from apps.users.models import Usuario
        usuario = Usuario.objects.get(user=request.user)
        
        service = NotificacionService()
        count = service.contar_no_leidas(usuario)
        
        return JsonResponse({
            'success': True,
            'new_count': count
        })
        
    except Exception as e:
        logger.error(f"Error verificando notificaciones: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)