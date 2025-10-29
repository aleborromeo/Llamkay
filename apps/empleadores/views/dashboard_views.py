from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

from apps.jobs.models import OfertaUsuario, OfertaEmpresa, Postulacion
from apps.users.models import Usuario


@login_required
def dashboard_empleador(request):
    """Dashboard principal del empleador"""
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
    )[:5]
    
    ofertas_activas_empresa = OfertaEmpresa.objects.filter(
        id_empleador=usuario,
        estado='activa'
    )[:5]
    
    # Postulaciones recientes
    postulaciones_recientes = Postulacion.objects.filter(
        Q(id_oferta_usuario__id_empleador=usuario) |
        Q(id_oferta_empresa__id_empleador=usuario)
    ).select_related(
        'id_trabajador',
        'id_oferta_usuario',
        'id_oferta_empresa'
    ).order_by('-fecha_postulacion')[:10]
    
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