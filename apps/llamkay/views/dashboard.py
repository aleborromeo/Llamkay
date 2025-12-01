"""
Vista de Dashboard con Integración de Soporte
"""
import logging
import random
from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, Sum
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


@login_required
def dashboard(request):
    """Vista principal del dashboard con manejo robusto de errores"""
    try:
        from apps.users.models import Usuario, Profile
        from apps.soporte.services import NotificacionService
        
        # ==================== OBTENER USUARIO ====================
        try:
            usuario_obj = Usuario.objects.select_related('profile_detalle').get(
                user=request.user
            )
        except Usuario.DoesNotExist:
            logger.error(f"❌ Usuario no encontrado para user: {request.user.id}")
            messages.error(request, "No se encontró tu perfil de usuario.")
            return redirect('users:completar_registro')
        
        # ==================== OBTENER O CREAR PROFILE ====================
        profile = getattr(usuario_obj, 'profile_detalle', None)
        if not profile:
            try:
                profile, created = Profile.objects.get_or_create(
                    id_usuario=usuario_obj,
                    defaults={
                        'bio': '',
                        'ocupacion': '',
                        'perfil_publico': True,
                        'mostrar_email': False,
                        'mostrar_telefono': False,
                    }
                )
                if created:
                    logger.info(f"✅ Profile creado automáticamente para {usuario_obj.email}")
            except Exception as e:
                logger.error(f"❌ Error creando profile: {e}")
                profile = None
        
        # ==================== NOTIFICACIONES ====================
        notificaciones_count = 0
        notificaciones_recientes = []
        try:
            notif_service = NotificacionService()
            notificaciones_count = notif_service.contar_no_leidas(usuario_obj)
            notificaciones_recientes = list(
                notif_service.obtener_no_leidas(usuario_obj)[:5]
            )
        except Exception as e:
            logger.warning(f"⚠️ Error cargando notificaciones: {str(e)}")
        
        # ==================== ESTADÍSTICAS ====================
        estadisticas = {
            'ofertas_activas': 0,
            'ofertas_totales': 0,
            'postulantes_totales': 0,
            'contratos_activos': 0,
            'vistas_totales': 0,
            'postulaciones_totales': 0,
            'tasa_aceptacion': 0,
            'mensajes_no_leidos': 0,
        }
        
        # Estadísticas según tipo de usuario
        try:
            if usuario_obj.tipo_usuario in ['empleador', 'trabajador_empleador', 'empresa']:
                from apps.jobs.models import OfertaUsuario, OfertaEmpresa, Postulacion, Contrato
                
                # Ofertas activas
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
                
                # Postulantes totales
                postulantes_usuario = Postulacion.objects.filter(
                    id_oferta_usuario__id_empleador=usuario_obj
                ).count()
                
                postulantes_empresa = Postulacion.objects.filter(
                    id_oferta_empresa__id_empleador=usuario_obj
                ).count()
                
                estadisticas['postulantes_totales'] = postulantes_usuario + postulantes_empresa
                
                # Contratos activos
                estadisticas['contratos_activos'] = Contrato.objects.filter(
                    id_empleador=usuario_obj,
                    estado='activo'
                ).count()
                
                # Vistas totales
                vistas_usuario = OfertaUsuario.objects.filter(
                    id_empleador=usuario_obj
                ).aggregate(total=Sum('vistas'))['total'] or 0
                
                vistas_empresa = OfertaEmpresa.objects.filter(
                    id_empleador=usuario_obj
                ).aggregate(total=Sum('vistas'))['total'] or 0
                
                estadisticas['vistas_totales'] = vistas_usuario + vistas_empresa
            
            # Estadísticas de trabajador
            if usuario_obj.tipo_usuario in ['trabajador', 'trabajador_empleador']:
                from apps.jobs.models import Postulacion
                
                estadisticas['postulaciones_totales'] = Postulacion.objects.filter(
                    id_trabajador=usuario_obj
                ).count()
                
                # Tasa de aceptación
                postulaciones_aceptadas = Postulacion.objects.filter(
                    id_trabajador=usuario_obj,
                    estado='aceptada'
                ).count()
                
                if estadisticas['postulaciones_totales'] > 0:
                    estadisticas['tasa_aceptacion'] = int(
                        (postulaciones_aceptadas / estadisticas['postulaciones_totales']) * 100
                    )
        except Exception as e:
            logger.error(f"❌ Error calculando estadísticas: {e}")
        
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
            logger.warning(f"⚠️ Error contando mensajes: {str(e)}")
        
        # ==================== ACTIVIDADES RECIENTES ====================
        actividades_recientes = []
        
        try:
            # Últimas postulaciones (trabajador)
            if usuario_obj.tipo_usuario in ['trabajador', 'trabajador_empleador']:
                from apps.jobs.models import Postulacion
                postulaciones = Postulacion.objects.filter(
                    id_trabajador=usuario_obj
                ).select_related('id_oferta_usuario', 'id_oferta_empresa').order_by('-created_at')[:5]
                
                for post in postulaciones:
                    titulo = 'Trabajo sin título'
                    if post.id_oferta_usuario:
                        titulo = post.id_oferta_usuario.titulo
                    elif post.id_oferta_empresa:
                        titulo = post.id_oferta_empresa.titulo_puesto
                    
                    actividades_recientes.append({
                        'tipo': 'info',
                        'mensaje': f'Postulaste a <strong>{titulo}</strong>',
                        'fecha': post.created_at
                    })
            
            # Últimas ofertas publicadas (empleador)
            if usuario_obj.tipo_usuario in ['empleador', 'trabajador_empleador', 'empresa']:
                from apps.jobs.models import OfertaUsuario, OfertaEmpresa
                
                ofertas_usuario = OfertaUsuario.objects.filter(
                    id_empleador=usuario_obj
                ).order_by('-created_at')[:3]
                
                for oferta in ofertas_usuario:
                    actividades_recientes.append({
                        'tipo': 'success',
                        'mensaje': f'Publicaste <strong>{oferta.titulo}</strong>',
                        'fecha': oferta.created_at
                    })
                
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
            logger.warning(f"⚠️ Error obteniendo actividades: {str(e)}")
        
        # Ordenar y limitar
        actividades_recientes.sort(key=lambda x: x['fecha'], reverse=True)
        actividades_recientes = actividades_recientes[:5]
        
        # ==================== TRABAJOS RECOMENDADOS ====================
        trabajos_recomendados = []
        
        try:
            if usuario_obj.tipo_usuario in ['trabajador', 'trabajador_empleador']:
                from apps.jobs.models import OfertaUsuario, OfertaEmpresa
                
                ofertas_usuario = list(OfertaUsuario.objects.filter(
                    estado='activa'
                ).exclude(
                    id_empleador=usuario_obj  # No mostrar propias ofertas
                ).select_related('id_empleador').order_by('-created_at')[:3])
                
                ofertas_empresa = list(OfertaEmpresa.objects.filter(
                    estado='activa'
                ).exclude(
                    id_empleador=usuario_obj
                ).select_related('id_empleador').order_by('-created_at')[:3])
                
                trabajos_recomendados = ofertas_usuario + ofertas_empresa
                trabajos_recomendados.sort(key=lambda x: x.created_at, reverse=True)
                trabajos_recomendados = trabajos_recomendados[:6]
        except Exception as e:
            logger.warning(f"⚠️ Error obteniendo trabajos: {str(e)}")
        
        # ==================== CONVERSACIONES RECIENTES ====================
        conversaciones_recientes = []
        
        try:
            from apps.chats.models import Conversacion
            conversaciones = Conversacion.objects.filter(
                Q(id_usuario_1=usuario_obj) | Q(id_usuario_2=usuario_obj)
            ).select_related('id_usuario_1', 'id_usuario_2').order_by('-updated_at')[:5]
            
            for conv in conversaciones:
                # Agregar el otro usuario a la conversación
                if conv.id_usuario_1 == usuario_obj:
                    conv.otro_usuario = conv.id_usuario_2
                else:
                    conv.otro_usuario = conv.id_usuario_1
                conversaciones_recientes.append(conv)
        except Exception as e:
            logger.warning(f"⚠️ Error obteniendo conversaciones: {str(e)}")
        
        # ==================== PERFIL COMPLETADO ====================
        perfil_completado = 0
        pasos_completados = 0
        total_pasos = 5
        
        # 1. Información básica
        if usuario_obj.nombres and usuario_obj.apellidos and usuario_obj.email:
            pasos_completados += 1
        
        # 2. Foto de perfil
        if hasattr(usuario_obj, 'foto') and usuario_obj.foto:
            pasos_completados += 1
        elif profile and hasattr(profile, 'foto_url') and profile.foto_url:
            pasos_completados += 1
                
        # 3. Teléfono
        if usuario_obj.telefono:
            pasos_completados += 1
        
        # 4. Bio/Descripción
        if profile and profile.bio:
            pasos_completados += 1
        
        # 5. Habilidades
        try:
            from apps.users.models import UsuarioHabilidad
            if UsuarioHabilidad.objects.filter(id_usuario=usuario_obj).exists():
                pasos_completados += 1
        except Exception:
            pass
        
        perfil_completado = int((pasos_completados / total_pasos) * 100)
        
        # ==================== CONSEJO DEL DÍA ====================
        consejos = [
            "Responde rápido a los mensajes para aumentar tus posibilidades de conseguir trabajos.",
            "Completa tu perfil al 100% para generar más confianza.",
            "Agrega certificaciones para destacar tu experiencia.",
            "Mantén actualizada tu disponibilidad.",
            "Las buenas calificaciones te ayudan a conseguir más oportunidades.",
            "Actualiza tu foto de perfil para dar una mejor impresión.",
            "Revisa tus notificaciones regularmente.",
        ]
        
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
            f"✅ Dashboard cargado: {usuario_obj.nombres} {usuario_obj.apellidos} - "
            f"Tipo: {usuario_obj.tipo_usuario}, "
            f"Perfil: {perfil_completado}%, "
            f"Notif: {notificaciones_count}"
        )
        
        return render(request, 'llamkay/dashboard.html', context)
        
    except Exception as e:
        logger.error(f"❌ Error crítico en dashboard: {str(e)}", exc_info=True)
        messages.error(request, "Ocurrió un error al cargar el dashboard. Por favor, intenta nuevamente.")
        
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