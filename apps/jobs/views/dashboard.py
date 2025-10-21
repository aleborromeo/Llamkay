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
        
        # Verificar que sea trabajador
        if usuario.tipo_usuario not in ['trabajador', 'ambos']:
            messages.error(request, "No tienes acceso a este dashboard.")
            return redirect('llamkay:dashboard')
        
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
        ).order_by('-fecha_postulacion')[:5]
        
        # Recomendaciones (trabajos nuevos según categorías de interés)
        # TODO: Implementar sistema de recomendaciones basado en perfil
        
        trabajos_recomendados = list(
            OfertaUsuario.objects.filter(
                estado='activa',
                deleted_at__isnull=True
            ).order_by('-fecha_publicacion')[:6]
        ) + list(
            OfertaEmpresa.objects.filter(
                estado='activa',
                deleted_at__isnull=True
            ).order_by('-fecha_publicacion')[:6]
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