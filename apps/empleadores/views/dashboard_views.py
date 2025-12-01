from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.users.models import Usuario
from apps.empleadores.services import DashboardService


dashboard_service = DashboardService()


@login_required
def dashboard_empleador(request):
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        if usuario.tipo_usuario not in ['empleador', 'ambos', 'empresa']:
            messages.error(request, "No tienes acceso a este dashboard.")
            return redirect('llamkay:dashboard')
        
        estadisticas = dashboard_service.get_estadisticas_dashboard(usuario.id_usuario)
        ofertas_recientes = dashboard_service.get_ofertas_recientes(usuario.id_usuario, limit=5)
        postulaciones_recientes = dashboard_service.get_postulaciones_recientes(usuario.id_usuario, limit=10)
        
        context = {
            'usuario': usuario,
            'estadisticas': estadisticas,
            'ofertas_recientes': ofertas_recientes,
            'postulaciones_recientes': postulaciones_recientes,
        }
        
        return render(request, 'empleadores/dashboard.html', context)
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')