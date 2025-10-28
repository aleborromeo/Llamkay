from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q

from apps.jobs.models import (
    OfertaUsuario, OfertaEmpresa, Postulacion,
    GuardarTrabajo, Contrato
)
from apps.users.models import Usuario


@login_required
def dashboard_trabajador(request):
    """Dashboard principal para trabajadores"""
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        # ✅ Validación opcional del tipo de usuario
        # if hasattr(usuario, 'tipo_usuario') and usuario.tipo_usuario not in ['trabajador', 'ambos']:
        #     messages.error(request, "No tienes acceso a este dashboard.")
        #     return redirect('llamkay:dashboard')
        
        # Estadísticas
        total_postulaciones = Postulacion.objects.filter(
            id_trabajador=usuario
        ).count()
        
        postulaciones_pendientes = Postulacion.objects.filter(
            id_trabajador=usuario,
            estado='pendiente'
        ).count()
        
        postulaciones_aceptadas = Postulacion.objects.filter(
            id_trabajador=usuario,
            estado='aceptada'
        ).count()
        
        trabajos_guardados = GuardarTrabajo.objects.filter(
            id_usuario=usuario
        ).count()
        
        contratos_activos = Contrato.objects.filter(
            id_trabajador=usuario,
            estado='activo'
        ).count()
        
        # Postulaciones recientes
        postulaciones_recientes = Postulacion.objects.filter(
            id_trabajador=usuario
        ).select_related(
            'id_oferta_usuario',
            'id_oferta_empresa'
        ).order_by('-created_at')[:5]  # ✅ Cambiado de fecha_postulacion
        
        # Recomendaciones (trabajos nuevos)
        trabajos_recomendados = list(
            OfertaUsuario.objects.filter(
                estado='activa',
            ).order_by('-created_at')[:6]  # ✅ Cambiado
        ) + list(
            OfertaEmpresa.objects.filter(
                estado='activa',
            ).order_by('-created_at')[:6]  # ✅ Cambiado
        )
        
        context = {
            'usuario': usuario,
            'estadisticas': {
                'total_postulaciones': total_postulaciones,
                'postulaciones_pendientes': postulaciones_pendientes,
                'postulaciones_aceptadas': postulaciones_aceptadas,
                'trabajos_guardados': trabajos_guardados,
                'contratos_activos': contratos_activos,
            },
            'postulaciones_recientes': postulaciones_recientes,
            'trabajos_recomendados': trabajos_recomendados[:12],
        }
        
        return render(request, 'jobs/dashboard/trabajador.html', context)
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')


@login_required
def dashboard_empleador(request):
    """Dashboard principal del empleador"""
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        # Estadísticas
        total_ofertas_usuario = OfertaUsuario.objects.filter(
            id_empleador=usuario
        ).count()
        
        total_ofertas_empresa = OfertaEmpresa.objects.filter(
            id_empleador=usuario
        ).count()
        
        total_postulaciones = Postulacion.objects.filter(
            Q(id_oferta_usuario__id_empleador=usuario) |
            Q(id_oferta_empresa__id_empleador=usuario)
        ).count()
        
        postulaciones_pendientes = Postulacion.objects.filter(
            Q(id_oferta_usuario__id_empleador=usuario) |
            Q(id_oferta_empresa__id_empleador=usuario),
            estado='pendiente'
        ).count()
        
        # Ofertas activas
        ofertas_activas_usuario = OfertaUsuario.objects.filter(
            id_empleador=usuario,
            estado='activa'
        ).order_by('-created_at')[:5]  # ✅ Agregado order_by
        
        ofertas_activas_empresa = OfertaEmpresa.objects.filter(
            id_empleador=usuario,
            estado='activa'
        ).order_by('-created_at')[:5]  # ✅ Agregado order_by
        
        # Postulaciones recientes
        postulaciones_recientes = Postulacion.objects.filter(
            Q(id_oferta_usuario__id_empleador=usuario) |
            Q(id_oferta_empresa__id_empleador=usuario)
        ).select_related(
            'id_trabajador',
            'id_oferta_usuario',
            'id_oferta_empresa'
        ).order_by('-created_at')[:10] 
        
        context = {
            'usuario': usuario,
            'estadisticas': {
                'total_ofertas_usuario': total_ofertas_usuario,
                'total_ofertas_empresa': total_ofertas_empresa,
                'total_ofertas': total_ofertas_usuario + total_ofertas_empresa,
                'total_postulaciones': total_postulaciones,
                'postulaciones_pendientes': postulaciones_pendientes,
            },
            'ofertas_activas_usuario': ofertas_activas_usuario,
            'ofertas_activas_empresa': ofertas_activas_empresa,
            'postulaciones_recientes': postulaciones_recientes,
        }
        
        return render(request, 'empleadores/dashboard.html', context)
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')