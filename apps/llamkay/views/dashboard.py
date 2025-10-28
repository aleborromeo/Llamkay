"""
Vista de Dashboard con Integración de Soporte
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
import logging

logger = logging.getLogger(__name__)


@login_required
def dashboard(request):
    """Vista principal del dashboard"""
    try:
        from apps.users.models import Usuario, Profile
        from apps.soporte.services import NotificacionService
        
        # ==================== OBTENER USUARIO ====================
        try:
            usuario_obj = Usuario.objects.select_related(
                'profile_detalle',
                'estadisticas'
            ).get(user=request.user)
        except Usuario.DoesNotExist:
            messages.error(request, "No se encontró tu perfil de usuario.")
            return redirect('users:login')
        
        # ✅ CORRECCIÓN: Obtener o crear Profile correctamente
        profile = getattr(usuario_obj, 'profile_detalle', None)
        if not profile:
            profile, _ = Profile.objects.get_or_create(
                id_usuario=usuario_obj,
                defaults={
                    'bio': '',
                    'ocupacion': '',
                    'perfil_publico': True,
                }
            )
        
        # ==================== NOTIFICACIONES (SOPORTE) ====================
        try:
            notif_service = NotificacionService()
            notificaciones_count = notif_service.contar_no_leidas(usuario_obj)
            notificaciones_recientes = list(
                notif_service.obtener_no_leidas(usuario_obj)[:5]
            )
        except Exception as e:
            logger.warning(f"Error cargando notificaciones: {str(e)}")
            notificaciones_count = 0
            notificaciones_recientes = []
        
        # ==================== ESTADÍSTICAS ====================
        estadisticas = {}
        
        # Obtener estadísticas según tipo de usuario
        if usuario_obj.tipo_usuario in ['empleador', 'ambos', 'empresa']:
            # Estadísticas para empleadores
            from apps.jobs.models import OfertaUsuario, OfertaEmpresa, Postulacion
            
            # Contar ofertas de ambos tipos
            ofertas_usuario_activas = OfertaUsuario.objects.filter(
                id_empleador=usuario_obj,
                estado='activa'
            ).count()
            
            ofertas_empresa_activas = OfertaEmpresa.objects.filter(
                id_empleador=usuario_obj,
                estado='activa'
            ).count()
            
            estadisticas['ofertas_activas'] = ofertas_usuario_activas + ofertas_empresa_activas
            
            # Total de ofertas
            ofertas_usuario_totales = OfertaUsuario.objects.filter(
                id_empleador=usuario_obj
            ).count()
            
            ofertas_empresa_totales = OfertaEmpresa.objects.filter(
                id_empleador=usuario_obj
            ).count()
            
            estadisticas['ofertas_totales'] = ofertas_usuario_totales + ofertas_empresa_totales
            
            # Postulantes totales (de ambos tipos de ofertas)
            postulantes_usuario = Postulacion.objects.filter(
                id_oferta_usuario__id_empleador=usuario_obj
            ).count()
            
            postulantes_empresa = Postulacion.objects.filter(
                id_oferta_empresa__id_empleador=usuario_obj
            ).count()
            
            estadisticas['postulantes_totales'] = postulantes_usuario + postulantes_empresa
            
            # Contratos activos
            from apps.jobs.models import Contrato
            estadisticas['contratos_activos'] = Contrato.objects.filter(
                id_empleador=usuario_obj,
                estado='activo'
            ).count()
            
            # Vistas totales
            vistas_usuario = OfertaUsuario.objects.filter(
                id_empleador=usuario_obj
            ).aggregate(total=Count('vistas'))['total'] or 0
            
            vistas_empresa = OfertaEmpresa.objects.filter(
                id_empleador=usuario_obj
            ).aggregate(total=Count('vistas'))['total'] or 0
            
            estadisticas['vistas_totales'] = vistas_usuario + vistas_empresa
            
        else:
            # Estadísticas para trabajadores
            from apps.jobs.models import Postulacion
            
            estadisticas['postulaciones_totales'] = Postulacion.objects.filter(
                id_trabajador=usuario_obj
            ).count()
            
            # Calcular tasa de aceptación
            postulaciones_aceptadas = Postulacion.objects.filter(
                id_trabajador=usuario_obj,
                estado='aceptada'
            ).count()
            
            if estadisticas['postulaciones_totales'] > 0:
                estadisticas['tasa_aceptacion'] = int(
                    (postulaciones_aceptadas / estadisticas['postulaciones_totales']) * 100
                )
            else:
                estadisticas['tasa_aceptacion'] = 0
        
        # Mensajes no leídos
        try:
            from apps.chats.models import Conversacion, Mensaje
            mensajes_no_leidos = Mensaje.objects.filter(
                id_conversacion__in=Conversacion.objects.filter(
                    Q(id_usuario_1=usuario_obj) | Q(id_usuario_2=usuario_obj)
                ),
                leido=False
            ).exclude(id_remitente=usuario_obj).count()
            
            estadisticas['mensajes_no_leidos'] = mensajes_no_leidos
        except Exception as e:
            logger.warning(f"Error contando mensajes: {str(e)}")
            estadisticas['mensajes_no_leidos'] = 0
        
        # ==================== ACTIVIDADES RECIENTES ====================
        actividades_recientes = []
        
        try:
            # Últimas postulaciones (si es trabajador)
            if usuario_obj.tipo_usuario in ['trabajador', 'ambos']:
                from apps.jobs.models import Postulacion
                postulaciones = Postulacion.objects.filter(
                    id_trabajador=usuario_obj
                ).select_related('id_oferta_usuario', 'id_oferta_empresa').order_by('-created_at')[:5]
                
                for post in postulaciones:
                    # Obtener el título de la oferta (puede ser de usuario o empresa)
                    titulo = ''
                    if post.id_oferta_usuario:
                        titulo = post.id_oferta_usuario.titulo
                    elif post.id_oferta_empresa:
                        titulo = post.id_oferta_empresa.titulo_puesto
                    
                    actividades_recientes.append({
                        'tipo': 'info',
                        'mensaje': f'Postulaste a <strong>{titulo}</strong>',
                        'fecha': post.created_at
                    })
            
            # Últimas ofertas publicadas (si es empleador)
            if usuario_obj.tipo_usuario in ['empleador', 'ambos', 'empresa']:
                from apps.jobs.models import OfertaUsuario, OfertaEmpresa
                
                # Ofertas de usuario
                ofertas_usuario = OfertaUsuario.objects.filter(
                    id_empleador=usuario_obj
                ).order_by('-created_at')[:3]
                
                for oferta in ofertas_usuario:
                    actividades_recientes.append({
                        'tipo': 'success',
                        'mensaje': f'Publicaste <strong>{oferta.titulo}</strong>',
                        'fecha': oferta.created_at
                    })
                
                # Ofertas de empresa
                ofertas_empresa = OfertaEmpresa.objects.filter(
                    id_empleador=usuario_obj
                ).order_by('-created_at')[:3]
                
                for oferta in ofertas_empresa:
                    actividades_recientes.append({
                        'tipo': 'success',
                        'mensaje': f'Publicaste <strong>{oferta.titulo_puesto}</strong>',
                        'fecha': oferta.created_at
                    })
        except Exception as e:
            logger.warning(f"Error obteniendo actividades: {str(e)}")
        
        # Ordenar por fecha y limitar a 5
        actividades_recientes.sort(key=lambda x: x['fecha'], reverse=True)
        actividades_recientes = actividades_recientes[:5]
        
        # ==================== TRABAJOS RECOMENDADOS ====================
        trabajos_recomendados = []
        
        try:
            if usuario_obj.tipo_usuario in ['trabajador', 'ambos']:
                from apps.jobs.models import OfertaUsuario, OfertaEmpresa
                
                # Obtener ofertas de usuario activas
                ofertas_usuario = list(OfertaUsuario.objects.filter(
                    estado='activa'
                ).select_related('id_empleador').order_by('-created_at')[:3])
                
                # Obtener ofertas de empresa activas
                ofertas_empresa = list(OfertaEmpresa.objects.filter(
                    estado='activa'
                ).select_related('id_empleador').order_by('-created_at')[:3])
                
                # Combinar ambas listas
                trabajos_recomendados = ofertas_usuario + ofertas_empresa
                
                # Ordenar por fecha y limitar a 6
                trabajos_recomendados.sort(key=lambda x: x.created_at, reverse=True)
                trabajos_recomendados = trabajos_recomendados[:6]
        except Exception as e:
            logger.warning(f"Error obteniendo trabajos: {str(e)}")
        
        # ==================== CONVERSACIONES RECIENTES ====================
        conversaciones_recientes = []
        
        try:
            from apps.chats.models import Conversacion
            conversaciones = Conversacion.objects.filter(
                Q(id_usuario_1=usuario_obj) | Q(id_usuario_2=usuario_obj)
            ).select_related('id_usuario_1', 'id_usuario_2').order_by('-updated_at')[:5]
            
            # ✅ Agregar método para obtener el otro usuario
            for conv in conversaciones:
                if conv.id_usuario_1 == usuario_obj:
                    conv.otro_usuario = conv.id_usuario_2
                else:
                    conv.otro_usuario = conv.id_usuario_1
                conversaciones_recientes.append(conv)
                
        except Exception as e:
            logger.warning(f"Error obteniendo conversaciones: {str(e)}")
        
        # ==================== PERFIL COMPLETADO ====================
        perfil_completado = 0
        pasos_completados = 0
        total_pasos = 4
        
        # Información básica
        if usuario_obj.nombres and usuario_obj.apellidos and usuario_obj.email:
            pasos_completados += 1
        
        # Foto de perfil
        if profile and profile.foto_url:
            pasos_completados += 1
        
        # Verificación
        if hasattr(usuario_obj, 'verificado') and usuario_obj.verificado:
            pasos_completados += 1
        
        # Habilidades
        from apps.users.models import UsuarioHabilidad
        if UsuarioHabilidad.objects.filter(id_usuario=usuario_obj).exists():
            pasos_completados += 1
        
        perfil_completado = int((pasos_completados / total_pasos) * 100)
        
        # ==================== CONSEJO DEL DÍA ====================
        consejos = [
            "Responde rápido a los mensajes para aumentar tus posibilidades de conseguir trabajos.",
            "Completa tu perfil al 100% para generar más confianza.",
            "Agrega certificaciones para destacar tu experiencia.",
            "Mantén actualizada tu disponibilidad.",
            "Las buenas calificaciones te ayudan a conseguir más oportunidades.",
        ]
        
        import random
        consejo_del_dia = random.choice(consejos)
        
        # ==================== CONTEXTO ====================
        context = {
            'usuario': usuario_obj,
            'profile': profile,
            'estadisticas': estadisticas,
            'actividades_recientes': actividades_recientes,
            'trabajos_recomendados': trabajos_recomendados,
            'conversaciones_recientes': conversaciones_recientes,
            'notificaciones_count': notificaciones_count,
            'notificaciones_recientes': notificaciones_recientes,
            'perfil_completado': perfil_completado,
            'consejo_del_dia': consejo_del_dia,
        }
        
        logger.info(
            f"✅ Dashboard cargado: {usuario_obj.nombres} - "
            f"Ofertas: {estadisticas.get('ofertas_activas', 0)}, "
            f"Notif: {notificaciones_count}, "
            f"Perfil: {perfil_completado}%"
        )
        
        return render(request, 'llamkay/dashboard.html', context)
        
    except Exception as e:
        logger.error(f"❌ Error crítico en dashboard: {str(e)}", exc_info=True)
        messages.error(request, "Ocurrió un error al cargar el dashboard")
        
        # Contexto mínimo de emergencia
        context = {
            'usuario': None,
            'profile': None,
            'estadisticas': {
                'ofertas_activas': 0,
                'postulantes_totales': 0,
                'mensajes_no_leidos': 0,
            },
            'actividades_recientes': [],
            'trabajos_recomendados': [],
            'conversaciones_recientes': [],
            'notificaciones_count': 0,
            'notificaciones_recientes': [],
            'perfil_completado': 0,
            'consejo_del_dia': 'Bienvenido a Llamkay',
        }
        
        return render(request, 'llamkay/dashboard.html', context)