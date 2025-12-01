"""
Vistas de Trabajos Guardados
Responsabilidad: Controladores para guardar/quitar trabajos
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator

from apps.jobs.services import GuardadoService
from apps.users.models import Usuario


class GuardadoViews:
    """
    Vistas para gestión de trabajos guardados
    Principio de Responsabilidad Única (SOLID)
    """
    
    def __init__(self):
        self.service = GuardadoService()
    
    @method_decorator(login_required)
    def trabajos_guardados(self, request):
        """Lista de trabajos guardados por el usuario"""
        try:
            usuario = Usuario.objects.get(user=request.user)
            
            # Obtener trabajos guardados
            trabajos = self.service.get_trabajos_guardados(usuario.id_usuario)
            
            # Contar guardados
            total_guardados = self.service.contar_guardados(usuario.id_usuario)
            
            context = {
                'trabajos': trabajos,
                'total_guardados': total_guardados,
                'usuario': usuario,
            }
            
            return render(request, 'jobs/guardados/lista.html', context)
            
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
            return redirect('users:login')
    
    @method_decorator(login_required)
    @method_decorator(require_POST)
    def guardar_trabajo(self, request, tipo, oferta_id):
        """Guardar/Marcar trabajo como favorito"""
        try:
            usuario = Usuario.objects.get(user=request.user)
            
            # Validar tipo
            if tipo not in ['usuario', 'empresa']:
                return JsonResponse({
                    'success': False,
                    'message': 'Tipo de oferta inválido'
                }, status=400)
            
            # Guardar trabajo
            resultado = self.service.guardar_trabajo(
                usuario.id_usuario,
                oferta_id,
                tipo
            )
            
            # Respuesta AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(resultado)
            
            # Respuesta normal
            if resultado['success']:
                messages.success(request, resultado['message'])
            else:
                messages.error(request, resultado['message'])
            
            return redirect('jobs:detalle_trabajo', tipo=tipo, trabajo_id=oferta_id)
            
        except Usuario.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Usuario no encontrado'
            }, status=404)
    
    @method_decorator(login_required)
    @method_decorator(require_POST)
    def quitar_guardado(self, request, guardado_id):
        """Quitar trabajo de guardados"""
        try:
            usuario = Usuario.objects.get(user=request.user)
            
            resultado = self.service.quitar_guardado(guardado_id, usuario.id_usuario)
            
            # Respuesta AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(resultado)
            
            # Respuesta normal
            if resultado['success']:
                messages.success(request, resultado['message'])
            else:
                messages.error(request, resultado['message'])
            
            return redirect('jobs:trabajos_guardados')
            
        except Usuario.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Usuario no encontrado'
            }, status=404)
    
    @method_decorator(login_required)
    def trabajos_guardados_ajax(self, request):
        """Cargar trabajos guardados con AJAX (para dashboard)"""
        try:
            usuario = Usuario.objects.get(user=request.user)
            
            # Obtener últimos 10 guardados
            trabajos = self.service.get_trabajos_guardados(usuario.id_usuario)[:10]
            
            trabajos_data = []
            for trabajo in trabajos:
                trabajos_data.append({
                    'guardado_id': trabajo['guardado_id'],
                    'tipo': trabajo['tipo'],
                    'id': trabajo['id'],
                    'titulo': trabajo['titulo'],
                    'pago': str(trabajo['pago']) if trabajo['pago'] else None,
                    'estado': trabajo['estado'],
                    'fecha_guardado': trabajo['fecha_guardado'].strftime('%d/%m/%Y %H:%M'),
                })
            
            return JsonResponse({
                'success': True,
                'trabajos': trabajos_data,
                'total': len(trabajos_data)
            })
            
        except Usuario.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'Usuario no encontrado'
            }, status=404)


# Instancia global
guardado_views = GuardadoViews()