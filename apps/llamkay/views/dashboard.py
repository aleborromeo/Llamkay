from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg, Sum
from django.utils import timezone
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)


@login_required
def dashboard(request):
    """Vista principal del dashboard adaptada al tipo de usuario"""
    
    try:
        # Obtener el Usuario personalizado desde el User de Django
        from apps.users.models import Usuario, Profile, UsuarioHabilidad
        
        # ❌ ERROR AQUÍ: Sobrescribes la variable usuario
        # from apps.core.templatetags.usuarios_extras import usuario  # ❌ ELIMINAR ESTA LÍNEA
        
        # ✅ CORRECTO: Obtener el usuario desde la base de datos
        usuario_obj = Usuario.objects.select_related('profile').get(user=request.user)
        profile, _ = Profile.objects.get_or_create(
            user=request.user,
            defaults={'id_usuario': usuario_obj}
        )
        
        # ==================== ESTADÍSTICAS GENERALES ====================
        estadisticas = {}
        actividades_recientes = []
        trabajos_recomendados = []
        conversaciones_recientes = []
        notificaciones_count = 0
        
        # ==================== MENSAJES NO LEÍDOS ====================
        try:
            from apps.chats.models import Conversacion, Mensaje
            
            # Obtener conversaciones del usuario
            conversaciones = Conversacion.objects.filter(
                Q(id_usuario_1=usuario_obj) | Q(id_usuario_2=usuario_obj),
                activa=True
            ).select_related('id_usuario_1', 'id_usuario_2').order_by('-ultimo_mensaje_at')
            
            mensajes_no_leidos = 0
            for conv in conversaciones[:5]:
                otro_usuario = conv.obtener_otro_usuario(usuario_obj)
                
                # Contar mensajes no leídos en esta conversación
                no_leidos = Mensaje.objects.filter(
                    id_conversacion=conv,
                    leido=False
                ).exclude(id_remitente=usuario_obj).count()
                
                mensajes_no_leidos += no_leidos
                
                # Guardar para el sidebar
                if len(conversaciones_recientes) < 5:
                    ultimo_msg = Mensaje.objects.filter(
                        id_conversacion=conv,
                        eliminado=False
                    ).order_by('-fecha_envio').first()
                    
                    conversaciones_recientes.append({
                        'id_conversacion': conv.id_conversacion,
                        'otro_usuario': otro_usuario,
                        'ultimo_mensaje': ultimo_msg.contenido[:50] if ultimo_msg else '',
                        'fecha': ultimo_msg.fecha_envio if ultimo_msg else conv.created_at,
                        'no_leidos': no_leidos
                    })
            
            estadisticas['mensajes_no_leidos'] = mensajes_no_leidos
            notificaciones_count = mensajes_no_leidos
            
        except Exception as e:
            logger.error(f"Error cargando mensajes: {str(e)}")
            estadisticas['mensajes_no_leidos'] = 0
        
        # ==================== ESTADÍSTICAS POR TIPO DE USUARIO ====================
        
        if usuario_obj.tipo_usuario in ['trabajador', 'ambos']:
            # ESTADÍSTICAS PARA TRABAJADORES
            try:
                from apps.jobs.models import Postulacion, GuardarTrabajo, Contrato
                
                # Total de postulaciones
                postulaciones_totales = Postulacion.objects.filter(
                    id_trabajador=usuario_obj
                ).count()
                
                estadisticas['postulaciones_totales'] = postulaciones_totales
                
                # Postulaciones pendientes
                estadisticas['postulaciones_pendientes'] = Postulacion.objects.filter(
                    id_trabajador=usuario_obj,
                    estado='pendiente'
                ).count()
                
                # Postulaciones aceptadas
                estadisticas['postulaciones_aceptadas'] = Postulacion.objects.filter(
                    id_trabajador=usuario_obj,
                    estado='aceptada'
                ).count()
                
                # Trabajos guardados
                estadisticas['trabajos_guardados'] = GuardarTrabajo.objects.filter(
                    id_usuario=usuario_obj
                ).count()
                
                # Contratos activos
                estadisticas['contratos_activos'] = Contrato.objects.filter(
                    id_trabajador=usuario_obj,
                    estado='activo'
                ).count()
                
                # Calcular tasa de aceptación
                if postulaciones_totales > 0:
                    tasa = (estadisticas['postulaciones_aceptadas'] / postulaciones_totales) * 100
                    estadisticas['tasa_aceptacion'] = round(tasa, 1)
                else:
                    estadisticas['tasa_aceptacion'] = 0
                
                # Tiempo de respuesta promedio (simulado - implementar según tu lógica)
                estadisticas['tiempo_respuesta'] = "2.5 hrs"
                
                # ==================== ACTIVIDADES RECIENTES (TRABAJADOR) ====================
                
                # Postulaciones aceptadas recientes
                postulaciones_aceptadas = Postulacion.objects.filter(
                    id_trabajador=usuario_obj,
                    estado='aceptada'
                ).select_related(
                    'id_oferta_usuario__id_empleador',
                    'id_oferta_empresa__id_empleador'
                ).order_by('-updated_at')[:2]
                
                for post in postulaciones_aceptadas:
                    if post.id_oferta_usuario:
                        empleador = post.id_oferta_usuario.id_empleador
                        titulo = post.id_oferta_usuario.titulo
                    else:
                        empleador = post.id_oferta_empresa.id_empleador
                        titulo = post.id_oferta_empresa.titulo_puesto
                    
                    actividades_recientes.append({
                        'tipo': 'success',
                        'mensaje': f'<strong>{empleador.nombres} {empleador.apellidos}</strong> aceptó tu propuesta para <strong>{titulo}</strong>',
                        'fecha': post.updated_at
                    })
                
                # Nuevos mensajes
                mensajes_nuevos = Mensaje.objects.filter(
                    id_conversacion__in=conversaciones,
                    leido=False
                ).exclude(id_remitente=usuario_obj).select_related('id_remitente').order_by('-fecha_envio')[:2]
                
                for msg in mensajes_nuevos:
                    actividades_recientes.append({
                        'tipo': 'info',
                        'mensaje': f'Nuevo mensaje de <strong>{msg.id_remitente.nombres} {msg.id_remitente.apellidos}</strong>',
                        'fecha': msg.fecha_envio
                    })
                
                # Calificaciones recientes
                from apps.jobs.models import Calificacion
                calificaciones_nuevas = Calificacion.objects.filter(
                    id_receptor=usuario_obj,
                    activa=True
                ).select_related('id_autor').order_by('-fecha')[:1]
                
                for cal in calificaciones_nuevas:
                    actividades_recientes.append({
                        'tipo': 'success',
                        'mensaje': f'Recibiste una calificación de <strong>{cal.puntuacion} estrellas</strong> de {cal.id_autor.nombres} {cal.id_autor.apellidos}',
                        'fecha': cal.fecha
                    })
                
                # Ordenar por fecha
                actividades_recientes.sort(key=lambda x: x['fecha'], reverse=True)
                
                # ==================== TRABAJOS RECOMENDADOS ====================
                from apps.jobs.models import OfertaUsuario, OfertaEmpresa
                
                # Obtener categorías de interés del usuario
                categorias_usuario = usuario_obj.usuariocategoria_set.values_list('id_categoria', flat=True)
                
                # Ofertas de usuarios
                ofertas_usuario = OfertaUsuario.objects.filter(
                    estado='activa',
                    deleted_at__isnull=True
                ).exclude(
                    id_empleador=usuario_obj
                ).select_related(
                    'id_empleador',
                    'id_categoria',
                    'id_departamento',
                    'id_provincia',
                    'id_distrito'
                ).order_by('-urgente', '-fecha_publicacion')[:6]
                
                for oferta in ofertas_usuario:
                    trabajos_recomendados.append({
                        'tipo': 'usuario',
                        'id': oferta.id,
                        'titulo': oferta.titulo,
                        'descripcion': oferta.descripcion,
                        'pago': oferta.pago,
                        'modalidad_pago': oferta.get_modalidad_pago_display(),
                        'urgente': oferta.urgente,
                        'fecha_publicacion': oferta.fecha_publicacion,
                        'empleador': oferta.id_empleador,
                        'categoria': oferta.id_categoria,
                        'ubicacion': {
                            'departamento': oferta.id_departamento.nombre if oferta.id_departamento else '',
                            'provincia': oferta.id_provincia.nombre if oferta.id_provincia else '',
                            'distrito': oferta.id_distrito.nombre if oferta.id_distrito else '',
                        }
                    })
                
                # Ofertas de empresas
                ofertas_empresa = OfertaEmpresa.objects.filter(
                    estado='activa',
                    deleted_at__isnull=True
                ).exclude(
                    id_empleador=usuario_obj
                ).select_related(
                    'id_empleador',
                    'id_categoria',
                    'id_departamento',
                    'id_provincia',
                    'id_distrito'
                ).order_by('-fecha_publicacion')[:6]
                
                for oferta in ofertas_empresa:
                    trabajos_recomendados.append({
                        'tipo': 'empresa',
                        'id': oferta.id,
                        'titulo': oferta.titulo_puesto,
                        'descripcion': oferta.descripcion,
                        'rango_salarial': oferta.rango_salarial,
                        'modalidad_trabajo': oferta.get_modalidad_trabajo_display(),
                        'fecha_publicacion': oferta.fecha_publicacion,
                        'empleador': oferta.id_empleador,
                        'categoria': oferta.id_categoria,
                        'ubicacion': {
                            'departamento': oferta.id_departamento.nombre if oferta.id_departamento else '',
                            'provincia': oferta.id_provincia.nombre if oferta.id_provincia else '',
                            'distrito': oferta.id_distrito.nombre if oferta.id_distrito else '',
                        },
                        'urgente': False
                    })
                
                # Mezclar y limitar a 12
                trabajos_recomendados = trabajos_recomendados[:12]
                
            except Exception as e:
                logger.error(f"Error cargando estadísticas de trabajador: {str(e)}")
        
        elif usuario_obj.tipo_usuario in ['empleador', 'empresa']:
            # ESTADÍSTICAS PARA EMPLEADORES/EMPRESAS
            try:
                from apps.jobs.models import OfertaUsuario, OfertaEmpresa, Postulacion, Contrato
                
                # Ofertas activas
                if usuario_obj.tipo_usuario == 'empresa':
                    ofertas_activas = OfertaEmpresa.objects.filter(
                        id_empleador=usuario_obj,
                        estado='activa',
                        deleted_at__isnull=True
                    ).count()
                    
                    ofertas_totales = OfertaEmpresa.objects.filter(
                        id_empleador=usuario_obj,
                        deleted_at__isnull=True
                    ).count()
                    
                    # Postulantes totales
                    postulantes_totales = Postulacion.objects.filter(
                        id_oferta_empresa__id_empleador=usuario_obj
                    ).count()
                    
                    # Vistas totales
                    vistas_totales = OfertaEmpresa.objects.filter(
                        id_empleador=usuario_obj
                    ).aggregate(total=Sum('vistas'))['total'] or 0
                    
                else:
                    ofertas_activas = OfertaUsuario.objects.filter(
                        id_empleador=usuario_obj,
                        estado='activa',
                        deleted_at__isnull=True
                    ).count()
                    
                    ofertas_totales = OfertaUsuario.objects.filter(
                        id_empleador=usuario_obj,
                        deleted_at__isnull=True
                    ).count()
                    
                    postulantes_totales = Postulacion.objects.filter(
                        id_oferta_usuario__id_empleador=usuario_obj
                    ).count()
                    
                    vistas_totales = OfertaUsuario.objects.filter(
                        id_empleador=usuario_obj
                    ).aggregate(total=Sum('vistas'))['total'] or 0
                
                estadisticas['ofertas_activas'] = ofertas_activas
                estadisticas['ofertas_totales'] = ofertas_totales
                estadisticas['postulantes_totales'] = postulantes_totales
                estadisticas['vistas_totales'] = vistas_totales
                
                # Contratos activos
                estadisticas['contratos_activos'] = Contrato.objects.filter(
                    id_empleador=usuario_obj,
                    estado='activo'
                ).count()
                
                # ==================== ACTIVIDADES RECIENTES (EMPLEADOR) ====================
                
                # Nuevas postulaciones
                if usuario_obj.tipo_usuario == 'empresa':
                    postulaciones_nuevas = Postulacion.objects.filter(
                        id_oferta_empresa__id_empleador=usuario_obj,
                        estado='pendiente'
                    ).select_related(
                        'id_trabajador',
                        'id_oferta_empresa'
                    ).order_by('-fecha_postulacion')[:3]
                else:
                    postulaciones_nuevas = Postulacion.objects.filter(
                        id_oferta_usuario__id_empleador=usuario_obj,
                        estado='pendiente'
                    ).select_related(
                        'id_trabajador',
                        'id_oferta_usuario'
                    ).order_by('-fecha_postulacion')[:3]
                
                for post in postulaciones_nuevas:
                    trabajador = post.id_trabajador
                    if post.id_oferta_usuario:
                        titulo = post.id_oferta_usuario.titulo
                    else:
                        titulo = post.id_oferta_empresa.titulo_puesto
                    
                    actividades_recientes.append({
                        'tipo': 'info',
                        'mensaje': f'<strong>{trabajador.nombres} {trabajador.apellidos}</strong> postuló a <strong>{titulo}</strong>',
                        'fecha': post.fecha_postulacion
                    })
                
                # ==================== POSTULANTES RECIENTES ====================
                trabajos_recomendados = []
                
                for post in postulaciones_nuevas[:6]:
                    trabajador = post.id_trabajador
                    if post.id_oferta_usuario:
                        oferta_titulo = post.id_oferta_usuario.titulo
                    else:
                        oferta_titulo = post.id_oferta_empresa.titulo_puesto
                    
                    trabajos_recomendados.append({
                        'tipo': 'postulante',
                        'id': post.id_postulacion,
                        'titulo': f"{trabajador.nombres} {trabajador.apellidos}",
                        'descripcion': f"Postuló a: {oferta_titulo}",
                        'pago': post.pretension_salarial,
                        'fecha_publicacion': post.fecha_postulacion,
                        'empleador': trabajador,
                        'categoria': None,
                        'ubicacion': {
                            'departamento': '',
                            'provincia': '',
                            'distrito': '',
                        },
                        'urgente': not post.leida
                    })
                
            except Exception as e:
                logger.error(f"Error cargando estadísticas de empleador: {str(e)}")
        
        # ==================== PERFIL COMPLETADO ====================
        perfil_completado = 0
        tareas_completadas = 0
        tareas_totales = 4
        
        # Información básica
        if usuario_obj.nombres and usuario_obj.apellidos:
            tareas_completadas += 1
        
        # Foto de perfil
        if profile.foto_url:
            tareas_completadas += 1
        
        # Verificación
        if usuario_obj.estado_verificacion == 'verificado':
            tareas_completadas += 1
        
        # Habilidades (solo para trabajadores)
        if usuario_obj.tipo_usuario in ['trabajador', 'ambos']:
            if UsuarioHabilidad.objects.filter(id_usuario=usuario_obj).exists():
                tareas_completadas += 1
        else:
            tareas_completadas += 1  # No aplica para empleadores
        
        perfil_completado = int((tareas_completadas / tareas_totales) * 100)
        
        # ==================== CONSEJO DEL DÍA ====================
        consejos = [
            "Responde rápido a los mensajes para aumentar tus posibilidades de conseguir trabajos.",
            "Mantén tu perfil actualizado con tus habilidades y experiencia más reciente.",
            "Las fotos de perfil profesionales aumentan tu credibilidad en un 60%.",
            "Completa tu verificación de identidad para destacar entre otros candidatos.",
            "Los trabajadores verificados reciben 3 veces más ofertas de trabajo."
        ]
        
        import random
        consejo_del_dia = random.choice(consejos)
        
        # ==================== CONTEXTO FINAL ====================
        context = {
            'usuario': usuario_obj,  # ✅ Usar usuario_obj en lugar de usuario
            'profile': profile,
            'estadisticas': estadisticas,
            'actividades_recientes': actividades_recientes[:5],
            'trabajos_recomendados': trabajos_recomendados,
            'conversaciones_recientes': conversaciones_recientes,
            'notificaciones_count': notificaciones_count,
            'perfil_completado': perfil_completado,
            'consejo_del_dia': consejo_del_dia,
        }

    except Usuario.DoesNotExist:
        messages.error(request, "No se encontró tu perfil de usuario.")
        return redirect('users:login')
    except Exception as e:
        logger.error(f"Error en dashboard: {str(e)}")
        messages.error(request, f"Ocurrió un error al cargar el dashboard: {str(e)}")
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