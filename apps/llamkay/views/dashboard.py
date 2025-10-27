"""
Vista de Dashboard
SRP: Solo renderiza el template, delega lógica a helpers
OCP: Abierta a extensión sin modificar código
DIP: Depende de abstracciones (helpers), no de implementaciones
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import logging

from ..utils import (
    obtener_estadisticas_usuario,
    obtener_actividades_recientes,
    obtener_trabajos_recomendados,
    obtener_mensajes_no_leidos,
    calcular_perfil_completado,
    obtener_consejo_del_dia,
)

logger = logging.getLogger(__name__)


@login_required
def dashboard(request):
    """
    Vista principal del dashboard
    
    SRP: Solo coordina helpers y renderiza template
    OCP: Extendible agregando nuevos helpers
    DIP: Depende de helpers (abstracciones)
    """
    try:
        from apps.users.models import Usuario, Profile
        
        # Obtener usuario y profile
        usuario_obj = Usuario.objects.select_related('profile').get(user=request.user)
        profile, _ = Profile.objects.get_or_create(
            user=request.user,
            defaults={'id_usuario': usuario_obj}
        )
        
        # Obtener mensajes no leídos
        mensajes_no_leidos, conversaciones_recientes = obtener_mensajes_no_leidos(usuario_obj)
        
        # Obtener estadísticas según tipo de usuario
        estadisticas = obtener_estadisticas_usuario(usuario_obj)
        estadisticas['mensajes_no_leidos'] = mensajes_no_leidos
        
        # Obtener actividades recientes
        actividades_recientes = obtener_actividades_recientes(usuario_obj, conversaciones_recientes)
        
        # Obtener trabajos/postulantes recomendados
        trabajos_recomendados = obtener_trabajos_recomendados(usuario_obj)
        
        # Calcular perfil completado
        perfil_completado = calcular_perfil_completado(usuario_obj, profile)
        
        # Obtener consejo del día
        consejo_del_dia = obtener_consejo_del_dia()
        
        # Contexto para el template
        context = {
            'usuario': usuario_obj,
            'profile': profile,
            'estadisticas': estadisticas,
            'actividades_recientes': actividades_recientes[:5],
            'trabajos_recomendados': trabajos_recomendados,
            'conversaciones_recientes': conversaciones_recientes,
            'notificaciones_count': mensajes_no_leidos,
            'perfil_completado': perfil_completado,
            'consejo_del_dia': consejo_del_dia,
        }
        
    except Usuario.DoesNotExist:
        messages.error(request, "No se encontró tu perfil de usuario.")
        return redirect('users:login')
        
    except Exception as e:
        logger.error(f"Error en dashboard: {str(e)}")
        messages.error(request, f"Ocurrió un error al cargar el dashboard")
        
        # Contexto mínimo en caso de error
        context = {
            'usuario': None,
            'profile': None,
            'estadisticas': {},
            'actividades_recientes': [],
            'trabajos_recomendados': [],
            'conversaciones_recientes': [],
            'notificaciones_count': 0,
            'perfil_completado': 0,
            'consejo_del_dia': 'Bienvenido a Llamkay',
        }

    return render(request, 'llamkay/dashboard.html', context)