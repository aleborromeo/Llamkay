"""
Vistas de Dashboard
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q

from apps.jobs.models import OfertaUsuario, OfertaEmpresa, Postulacion, GuardarTrabajo, Contrato
from apps.jobs.utils import (
    obtener_trabajos_unificados,
    obtener_estadisticas_empleador,
    obtener_estadisticas_trabajador
)
from apps.users.models import Usuario


@login_required
def dashboard_trabajador(request):
    """
    Dashboard principal para trabajadores
    """
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        # Validar tipo de usuario
        if usuario.tipo_usuario not in ['trabajador', 'ambos']:
            messages.error(request, "No tienes acceso a este dashboard.")
            return redirect('llamkay:dashboard')
        
        # Obtener estadísticas
        estadisticas = obtener_estadisticas_trabajador(usuario)
        
        # Trabajos guardados
        trabajos_guardados = GuardarTrabajo.objects.filter(
            id_usuario=usuario
        ).count()
        
        # Contratos activos
        contratos_activos = Contrato.objects.filter(
            id_trabajador=usuario,
            estado='activo'
        ).count()
        
        # Agregar más estadísticas
        estadisticas.update({
            'trabajos_guardados': trabajos_guardados,
            'contratos_activos': contratos_activos,
        })
        
        # Postulaciones recientes
        postulaciones_recientes = Postulacion.objects.filter(
            id_trabajador=usuario
        ).select_related(
            'id_oferta_usuario',
            'id_oferta_usuario__id_empleador',
            'id_oferta_empresa',
            'id_oferta_empresa__id_empleador'
        ).order_by('-created_at')[:5]
        
        # Formatear postulaciones
        postulaciones_data = []
        for post in postulaciones_recientes:
            oferta = post.oferta
            tipo = post.tipo_oferta
            
            postulaciones_data.append({
                'id': post.id_postulacion,
                'tipo': tipo,
                'titulo': oferta.titulo if tipo == 'usuario' else oferta.titulo_puesto,
                'empleador': oferta.id_empleador.nombre_completo,
                'estado': post.estado,
                'estado_display': post.get_estado_display(),
                'fecha': post.created_at,
                'oferta_id': oferta.id,
            })
        
        # Trabajos recomendados (últimos publicados)
        trabajos_recomendados = obtener_trabajos_unificados(
            limit=6,
            usuario_actual=usuario
        )
        
        context = {
            'usuario': usuario,
            'estadisticas': estadisticas,
            'postulaciones_recientes': postulaciones_data,
            'trabajos_recomendados': trabajos_recomendados,
        }
        
        return render(request, 'jobs/dashboard/trabajador.html', context)
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')


@login_required
def dashboard_empleador(request):
    """
    Dashboard principal del empleador
    """
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        # Validar tipo de usuario
        if usuario.tipo_usuario not in ['empleador', 'ambos', 'empresa']:
            messages.error(request, "No tienes acceso a este dashboard.")
            return redirect('llamkay:dashboard')
        
        # Obtener estadísticas
        estadisticas = obtener_estadisticas_empleador(usuario)
        
        # Ofertas activas recientes
        ofertas_activas_usuario = OfertaUsuario.objects.filter(
            id_empleador=usuario,
            estado='activa'
        ).select_related(
            'id_categoria'
        ).annotate(
            postulaciones_count=Count('postulaciones')
        ).order_by('-created_at')[:5]
        
        ofertas_activas_empresa = OfertaEmpresa.objects.filter(
            id_empleador=usuario,
            estado='activa'
        ).select_related(
            'id_categoria'
        ).annotate(
            postulaciones_count=Count('postulaciones')
        ).order_by('-created_at')[:5]
        
        # Formatear ofertas
        ofertas_data = []
        
        for oferta in ofertas_activas_usuario:
            ofertas_data.append({
                'tipo': 'usuario',
                'id': oferta.id,
                'titulo': oferta.titulo,
                'estado': oferta.estado,
                'vistas': oferta.vistas,
                'postulaciones': oferta.postulaciones_count,
                'fecha': oferta.created_at,
            })
        
        for oferta in ofertas_activas_empresa:
            ofertas_data.append({
                'tipo': 'empresa',
                'id': oferta.id,
                'titulo': oferta.titulo_puesto,
                'estado': oferta.estado,
                'vistas': oferta.vistas,
                'postulaciones': oferta.postulaciones_count,
                'fecha': oferta.created_at,
            })
        
        # Ordenar por fecha
        ofertas_data.sort(key=lambda x: x['fecha'], reverse=True)
        
        # Postulaciones recientes
        postulaciones_recientes = Postulacion.objects.filter(
            Q(id_oferta_usuario__id_empleador=usuario) |
            Q(id_oferta_empresa__id_empleador=usuario)
        ).select_related(
            'id_trabajador',
            'id_oferta_usuario',
            'id_oferta_empresa'
        ).order_by('-created_at')[:10]
        
        # Formatear postulaciones
        postulaciones_data = []
        for post in postulaciones_recientes:
            oferta = post.oferta
            tipo = post.tipo_oferta
            
            postulaciones_data.append({
                'id': post.id_postulacion,
                'tipo': tipo,
                'titulo': oferta.titulo if tipo == 'usuario' else oferta.titulo_puesto,
                'trabajador': post.id_trabajador.nombre_completo,
                'estado': post.estado,
                'estado_display': post.get_estado_display(),
                'fecha': post.created_at,
                'leida': post.leida,
                'oferta_id': oferta.id,
            })
        
        context = {
            'usuario': usuario,
            'estadisticas': estadisticas,
            'ofertas_activas': ofertas_data[:5],
            'postulaciones_recientes': postulaciones_data,
        }
        
        return render(request, 'jobs/dashboard/empleador.html', context)
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')


@login_required
def admin_empleador(request):
    """
    Panel de administración del empleador (alias de dashboard_empleador)
    """
    return dashboard_empleador(request)


@login_required
def admin_empresa(request):
    """
    Panel de administración de empresa (alias de dashboard_empleador)
    """
    return dashboard_empleador(request)