"""
Dashboard Helpers - Lógica de negocio para el dashboard
Cumple con SOLID:
- SRP: Cada función tiene una única responsabilidad
- OCP: Abierto a extensión, cerrado a modificación
- DIP: Depende de abstracciones (modelos), no de implementaciones
"""
from typing import Dict, Any, List, Tuple
from django.db.models import Q, Sum
import logging
import random

logger = logging.getLogger(__name__)


# ==================== MENSAJES ====================

def obtener_mensajes_no_leidos(usuario) -> Tuple[int, List[Dict]]:
    """
    Obtener mensajes no leídos y conversaciones recientes
    SRP: Solo maneja mensajes
    """
    try:
        from apps.chats.models import Conversacion, Mensaje
        
        conversaciones = Conversacion.objects.filter(
            Q(id_usuario_1=usuario) | Q(id_usuario_2=usuario),
            activa=True
        ).select_related('id_usuario_1', 'id_usuario_2').order_by('-ultimo_mensaje_at')
        
        mensajes_no_leidos = 0
        conversaciones_recientes = []
        
        for conv in conversaciones[:5]:
            otro_usuario = conv.obtener_otro_usuario(usuario)
            
            no_leidos = Mensaje.objects.filter(
                id_conversacion=conv,
                leido=False
            ).exclude(id_remitente=usuario).count()
            
            mensajes_no_leidos += no_leidos
            
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
        
        return mensajes_no_leidos, conversaciones_recientes
        
    except Exception as e:
        logger.error(f"Error obteniendo mensajes: {str(e)}")
        return 0, []


# ==================== ESTADÍSTICAS ====================

def obtener_estadisticas_usuario(usuario) -> Dict[str, Any]:
    """
    Obtener estadísticas según tipo de usuario
    SRP: Solo obtiene estadísticas
    OCP: Delega en funciones específicas
    """
    if usuario.tipo_usuario in ['trabajador', 'ambos']:
        return _calcular_estadisticas_trabajador(usuario)
    elif usuario.tipo_usuario in ['empleador', 'empresa']:
        return _calcular_estadisticas_empleador(usuario)
    return {}


def _calcular_estadisticas_trabajador(usuario) -> Dict[str, Any]:
    """Calcular estadísticas para trabajadores"""
    try:
        from apps.jobs.models import Postulacion, GuardarTrabajo, Contrato
        
        postulaciones_totales = Postulacion.objects.filter(
            id_trabajador=usuario
        ).count()
        
        postulaciones_aceptadas = Postulacion.objects.filter(
            id_trabajador=usuario,
            estado='aceptada'
        ).count()
        
        estadisticas = {
            'postulaciones_totales': postulaciones_totales,
            'postulaciones_pendientes': Postulacion.objects.filter(
                id_trabajador=usuario,
                estado='pendiente'
            ).count(),
            'postulaciones_aceptadas': postulaciones_aceptadas,
            'trabajos_guardados': GuardarTrabajo.objects.filter(
                id_usuario=usuario
            ).count(),
            'contratos_activos': Contrato.objects.filter(
                id_trabajador=usuario,
                estado='activo'
            ).count(),
        }
        
        # Calcular tasa de aceptación
        if postulaciones_totales > 0:
            tasa = (postulaciones_aceptadas / postulaciones_totales) * 100
            estadisticas['tasa_aceptacion'] = round(tasa, 1)
        else:
            estadisticas['tasa_aceptacion'] = 0
        
        estadisticas['tiempo_respuesta'] = "2.5 hrs"
        
        return estadisticas
        
    except Exception as e:
        logger.error(f"Error calculando estadísticas de trabajador: {str(e)}")
        return {}


def _calcular_estadisticas_empleador(usuario) -> Dict[str, Any]:
    """Calcular estadísticas para empleadores"""
    try:
        from apps.jobs.models import OfertaUsuario, OfertaEmpresa, Postulacion, Contrato
        
        if usuario.tipo_usuario == 'empresa':
            ofertas_activas = OfertaEmpresa.objects.filter(
                id_empleador=usuario,
                estado='activa',
                deleted_at__isnull=True
            ).count()
            
            ofertas_totales = OfertaEmpresa.objects.filter(
                id_empleador=usuario,
                deleted_at__isnull=True
            ).count()
            
            postulantes_totales = Postulacion.objects.filter(
                id_oferta_empresa__id_empleador=usuario
            ).count()
            
            vistas_totales = OfertaEmpresa.objects.filter(
                id_empleador=usuario
            ).aggregate(total=Sum('vistas'))['total'] or 0
            
        else:
            ofertas_activas = OfertaUsuario.objects.filter(
                id_empleador=usuario,
                estado='activa',
                deleted_at__isnull=True
            ).count()
            
            ofertas_totales = OfertaUsuario.objects.filter(
                id_empleador=usuario,
                deleted_at__isnull=True
            ).count()
            
            postulantes_totales = Postulacion.objects.filter(
                id_oferta_usuario__id_empleador=usuario
            ).count()
            
            vistas_totales = OfertaUsuario.objects.filter(
                id_empleador=usuario
            ).aggregate(total=Sum('vistas'))['total'] or 0
        
        return {
            'ofertas_activas': ofertas_activas,
            'ofertas_totales': ofertas_totales,
            'postulantes_totales': postulantes_totales,
            'vistas_totales': vistas_totales,
            'contratos_activos': Contrato.objects.filter(
                id_empleador=usuario,
                estado='activo'
            ).count(),
        }
        
    except Exception as e:
        logger.error(f"Error calculando estadísticas de empleador: {str(e)}")
        return {}


# ==================== ACTIVIDADES RECIENTES ====================

def obtener_actividades_recientes(usuario, conversaciones) -> List[Dict[str, Any]]:
    """
    Obtener actividades recientes según tipo de usuario
    SRP: Solo obtiene actividades
    OCP: Delega en funciones específicas
    """
    if usuario.tipo_usuario in ['trabajador', 'ambos']:
        return _obtener_actividades_trabajador(usuario, conversaciones)
    elif usuario.tipo_usuario in ['empleador', 'empresa']:
        return _obtener_actividades_empleador(usuario)
    return []


def _obtener_actividades_trabajador(usuario, conversaciones) -> List[Dict[str, Any]]:
    """Obtener actividades de trabajadores"""
    actividades = []
    
    try:
        from apps.jobs.models import Postulacion, Calificacion
        from apps.chats.models import Mensaje
        
        # Postulaciones aceptadas recientes
        postulaciones_aceptadas = Postulacion.objects.filter(
            id_trabajador=usuario,
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
            
            actividades.append({
                'tipo': 'success',
                'mensaje': f'<strong>{empleador.nombres} {empleador.apellidos}</strong> aceptó tu propuesta para <strong>{titulo}</strong>',
                'fecha': post.updated_at
            })
        
        # Nuevos mensajes
        mensajes_nuevos = Mensaje.objects.filter(
            id_conversacion__in=conversaciones,
            leido=False
        ).exclude(id_remitente=usuario).select_related('id_remitente').order_by('-fecha_envio')[:2]
        
        for msg in mensajes_nuevos:
            actividades.append({
                'tipo': 'info',
                'mensaje': f'Nuevo mensaje de <strong>{msg.id_remitente.nombres} {msg.id_remitente.apellidos}</strong>',
                'fecha': msg.fecha_envio
            })
        
        # Calificaciones recientes
        calificaciones_nuevas = Calificacion.objects.filter(
            id_receptor=usuario,
            activa=True
        ).select_related('id_autor').order_by('-fecha')[:1]
        
        for cal in calificaciones_nuevas:
            actividades.append({
                'tipo': 'success',
                'mensaje': f'Recibiste una calificación de <strong>{cal.puntuacion} estrellas</strong> de {cal.id_autor.nombres} {cal.id_autor.apellidos}',
                'fecha': cal.fecha
            })
        
        # Ordenar por fecha
        actividades.sort(key=lambda x: x['fecha'], reverse=True)
        
    except Exception as e:
        logger.error(f"Error obteniendo actividades de trabajador: {str(e)}")
    
    return actividades


def _obtener_actividades_empleador(usuario) -> List[Dict[str, Any]]:
    """Obtener actividades de empleadores"""
    actividades = []
    
    try:
        from apps.jobs.models import Postulacion
        
        if usuario.tipo_usuario == 'empresa':
            postulaciones_nuevas = Postulacion.objects.filter(
                id_oferta_empresa__id_empleador=usuario,
                estado='pendiente'
            ).select_related(
                'id_trabajador',
                'id_oferta_empresa'
            ).order_by('-fecha_postulacion')[:3]
        else:
            postulaciones_nuevas = Postulacion.objects.filter(
                id_oferta_usuario__id_empleador=usuario,
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
            
            actividades.append({
                'tipo': 'info',
                'mensaje': f'<strong>{trabajador.nombres} {trabajador.apellidos}</strong> postuló a <strong>{titulo}</strong>',
                'fecha': post.fecha_postulacion
            })
        
    except Exception as e:
        logger.error(f"Error obteniendo actividades de empleador: {str(e)}")
    
    return actividades


# ==================== TRABAJOS/POSTULANTES RECOMENDADOS ====================

def obtener_trabajos_recomendados(usuario) -> List[Dict[str, Any]]:
    """
    Obtener trabajos recomendados según tipo de usuario
    SRP: Solo obtiene recomendaciones
    OCP: Delega en funciones específicas
    """
    if usuario.tipo_usuario in ['trabajador', 'ambos']:
        return _obtener_trabajos_para_trabajador(usuario)
    elif usuario.tipo_usuario in ['empleador', 'empresa']:
        return _obtener_postulantes_para_empleador(usuario)
    return []


def _obtener_trabajos_para_trabajador(usuario) -> List[Dict[str, Any]]:
    """Obtener trabajos recomendados para trabajadores"""
    trabajos_recomendados = []
    
    try:
        from apps.jobs.models import OfertaUsuario, OfertaEmpresa
        
        # Ofertas de usuarios
        ofertas_usuario = OfertaUsuario.objects.filter(
            estado='activa',
            deleted_at__isnull=True
        ).exclude(
            id_empleador=usuario
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
            id_empleador=usuario
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
        
        return trabajos_recomendados[:12]
        
    except Exception as e:
        logger.error(f"Error obteniendo trabajos recomendados: {str(e)}")
        return []


def _obtener_postulantes_para_empleador(usuario) -> List[Dict[str, Any]]:
    """Obtener postulantes recientes para empleadores"""
    postulantes = []
    
    try:
        from apps.jobs.models import Postulacion
        
        if usuario.tipo_usuario == 'empresa':
            postulaciones_nuevas = Postulacion.objects.filter(
                id_oferta_empresa__id_empleador=usuario,
                estado='pendiente'
            ).select_related(
                'id_trabajador',
                'id_oferta_empresa'
            ).order_by('-fecha_postulacion')[:6]
        else:
            postulaciones_nuevas = Postulacion.objects.filter(
                id_oferta_usuario__id_empleador=usuario,
                estado='pendiente'
            ).select_related(
                'id_trabajador',
                'id_oferta_usuario'
            ).order_by('-fecha_postulacion')[:6]
        
        for post in postulaciones_nuevas:
            trabajador = post.id_trabajador
            if post.id_oferta_usuario:
                oferta_titulo = post.id_oferta_usuario.titulo
            else:
                oferta_titulo = post.id_oferta_empresa.titulo_puesto
            
            postulantes.append({
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
        logger.error(f"Error obteniendo postulantes: {str(e)}")
    
    return postulantes


# ==================== PERFIL ====================

def calcular_perfil_completado(usuario, profile) -> int:
    """
    Calcular porcentaje de perfil completado
    SRP: Solo calcula porcentaje
    """
    from apps.users.models import UsuarioHabilidad
    
    tareas_completadas = 0
    tareas_totales = 4
    
    # Información básica
    if usuario.nombres and usuario.apellidos:
        tareas_completadas += 1
    
    # Foto de perfil
    if profile.foto_url:
        tareas_completadas += 1
    
    # Verificación
    if usuario.estado_verificacion == 'verificado':
        tareas_completadas += 1
    
    # Habilidades (solo para trabajadores)
    if usuario.tipo_usuario in ['trabajador', 'ambos']:
        if UsuarioHabilidad.objects.filter(id_usuario=usuario).exists():
            tareas_completadas += 1
    else:
        tareas_completadas += 1  # No aplica para empleadores
    
    return int((tareas_completadas / tareas_totales) * 100)


# ==================== CONSEJOS ====================

def obtener_consejo_del_dia() -> str:
    """
    Obtener un consejo aleatorio del día
    SRP: Solo obtiene consejos
    """
    consejos = [
        "Responde rápido a los mensajes para aumentar tus posibilidades de conseguir trabajos.",
        "Mantén tu perfil actualizado con tus habilidades y experiencia más reciente.",
        "Las fotos de perfil profesionales aumentan tu credibilidad en un 60%.",
        "Completa tu verificación de identidad para destacar entre otros candidatos.",
        "Los trabajadores verificados reciben 3 veces más ofertas de trabajo."
    ]
    return random.choice(consejos)