from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
import logging

logger = logging.getLogger(__name__)


@login_required
def dashboard(request):
    """Vista principal del dashboard"""
    
    try:
        # Obtener el Usuario personalizado desde el User de Django
        from apps.users.models import Usuario, Profile
        
        usuario = Usuario.objects.get(user=request.user)
        profile, _ = Profile.objects.get_or_create(
            user=request.user,
            defaults={'id_usuario': usuario}
        )
        
        context = {
            'usuario': usuario,
            'profile': profile,
            'mensajes_recientes': [],
            'total_mensajes_no_leidos': 0,
            'trabajos_recientes': [],
        }

    except Usuario.DoesNotExist:
        messages.error(request, "No se encontró tu perfil de usuario.")
        return redirect('users:login')

    # Intentar cargar mensajes recientes
    try:
        from apps.chats.models import Chat, Mensaje
        
        # Obtener chats donde participa el usuario
        chats = Chat.objects.filter(
            Q(usuario_1=usuario) | Q(usuario_2=usuario)
        ).select_related('usuario_1', 'usuario_2').order_by('-fecha_creacion')[:5]
        
        mensajes_recientes = []
        total_no_leidos = 0
        
        for chat in chats:
            # Determinar el otro usuario
            otro_usuario = chat.usuario_2 if chat.usuario_1 == usuario else chat.usuario_1
            
            # Obtener último mensaje
            ultimo_mensaje_obj = chat.mensajes.order_by('-fecha_envio').first()
            
            if ultimo_mensaje_obj:
                # Contar mensajes no leídos
                no_leidos = chat.mensajes.filter(
                    destinatario=usuario,
                    leido=False
                ).count()
                
                total_no_leidos += no_leidos
                
                # Obtener iniciales
                iniciales = ""
                if hasattr(otro_usuario, 'nombres') and hasattr(otro_usuario, 'apellidos'):
                    iniciales = f"{otro_usuario.nombres[:1]}{otro_usuario.apellidos[:1]}".upper()
                else:
                    iniciales = otro_usuario.username[:2].upper()
                
                # Obtener foto
                foto_url = None
                if hasattr(otro_usuario, 'perfil') and otro_usuario.perfil.foto_url:
                    foto_url = otro_usuario.perfil.foto_url.url
                
                # Obtener nombre completo
                nombre_completo = ""
                if hasattr(otro_usuario, 'nombres') and hasattr(otro_usuario, 'apellidos'):
                    nombre_completo = f"{otro_usuario.nombres} {otro_usuario.apellidos}"
                else:
                    nombre_completo = otro_usuario.username
                
                mensajes_recientes.append({
                    'chat_id': chat.id_chat,
                    'otro_usuario': otro_usuario,
                    'nombre_otro_usuario': nombre_completo,
                    'foto_otro_usuario': foto_url,
                    'iniciales': iniciales,
                    'ultimo_mensaje': ultimo_mensaje_obj.contenido[:50],
                    'fecha_envio': ultimo_mensaje_obj.fecha_envio,
                    'no_leidos': no_leidos,
                })
        
        context['mensajes_recientes'] = mensajes_recientes
        context['total_mensajes_no_leidos'] = total_no_leidos
        
    except Exception as e:
        logger.error(f"Error cargando mensajes: {str(e)}")
        context['mensajes_recientes'] = []
        context['total_mensajes_no_leidos'] = 0

    # Intentar cargar trabajos recientes
    try:
        from apps.jobs.models import Trabajo
        
        # Obtener trabajos recientes según el tipo de usuario
        if hasattr(usuario, 'perfil'):
            tipo_usuario = usuario.perfil.tipo_usuario
            
            if tipo_usuario in ['buscar-trabajo', 'ambos']:
                # Trabajos disponibles para aplicar
                trabajos = Trabajo.objects.filter(
                    estado='activo'
                ).select_related('empleador').order_by('-fecha_publicacion')[:6]
                context['trabajos_recientes'] = trabajos
                
    except Exception as e:
        logger.error(f"Error cargando trabajos: {str(e)}")
        context['trabajos_recientes'] = []

    return render(request, 'llamkay/dashboard.html', context)