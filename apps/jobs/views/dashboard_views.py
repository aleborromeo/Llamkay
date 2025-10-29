"""
Vistas de Dashboard para Trabajadores
Responsabilidad: Controladores para dashboard de trabajadores
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.decorators import method_decorator

from apps.jobs.services import PostulacionService, GuardadoService, BusquedaService
from apps.jobs.models import Contrato
from apps.users.models import Usuario


class DashboardViews:
    """
    Vistas de dashboard para trabajadores
    Principio de Responsabilidad Única (SOLID)
    """
    
    def __init__(self):
        self.postulacion_service = PostulacionService()
        self.guardado_service = GuardadoService()
        self.busqueda_service = BusquedaService()
    
    @method_decorator(login_required)
    def dashboard_trabajador(self, request):
        """Dashboard principal para trabajadores"""
        try:
            usuario = Usuario.objects.get(user=request.user)
            
            # Validar tipo de usuario
            if usuario.tipo_usuario not in ['trabajador', 'ambos']:
                messages.error(request, "No tienes acceso a este dashboard.")
                return redirect('llamkay:dashboard')
            
            # Obtener estadísticas
            estadisticas = self.postulacion_service.get_estadisticas_trabajador(
                usuario.id_usuario
            )
            
            # Trabajos guardados
            trabajos_guardados = self.guardado_service.contar_guardados(usuario.id_usuario)
            
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
            postulaciones_recientes = self.postulacion_service.get_postulaciones_trabajador(
                usuario.id_usuario
            )[:5]
            
            # Trabajos recomendados
            trabajos_recomendados = self.busqueda_service.buscar_trabajos(
                filtros={},
                usuario_actual=usuario
            )[:6]
            
            context = {
                'usuario': usuario,
                'estadisticas': estadisticas,
                'postulaciones_recientes': postulaciones_recientes,
                'trabajos_recomendados': trabajos_recomendados,
            }
            
            return render(request, 'jobs/dashboard/trabajador.html', context)
            
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
            return redirect('users:login')


# Instancia global
dashboard_views = DashboardViews()