"""
Vistas de Postulaciones
Responsabilidad: Controladores para gestión de postulaciones
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from decimal import Decimal, InvalidOperation

from apps.jobs.services import PostulacionService, BusquedaService
from apps.jobs.models import OfertaUsuario, OfertaEmpresa
from apps.users.models import Usuario


class PostulacionViews:
    """
    Vistas para gestión de postulaciones
    Principio de Responsabilidad Única (SOLID)
    """
    
    def __init__(self):
        self.service = PostulacionService()
        self.busqueda_service = BusquedaService()
    
    @method_decorator(login_required)
    def postular_trabajo(self, request, tipo, oferta_id):
        """Postular a una oferta de trabajo"""
        try:
            usuario = Usuario.objects.get(user=request.user)
            
            # Validar que sea trabajador
            if usuario.tipo_usuario not in ['trabajador', 'ambos']:
                messages.error(request, "Solo los trabajadores pueden postular.")
                return redirect('jobs:buscar_trabajos')
            
            # Validar tipo
            if tipo not in ['usuario', 'empresa']:
                messages.error(request, "Tipo de oferta inválido.")
                return redirect('jobs:buscar_trabajos')
            
            # Obtener oferta
            if tipo == 'usuario':
                oferta = get_object_or_404(OfertaUsuario, id=oferta_id, estado='activa')
            else:
                oferta = get_object_or_404(OfertaEmpresa, id=oferta_id, estado='activa')
            
            if request.method == 'POST':
                mensaje = request.POST.get('mensaje', '').strip()
                pretension_salarial = request.POST.get('pretension_salarial')
                disponibilidad_inmediata = request.POST.get('disponibilidad_inmediata') == 'on'
                
                # Validar mensaje
                if not mensaje:
                    messages.error(request, "Debes incluir un mensaje de presentación.")
                    return redirect('jobs:postular_trabajo', tipo=tipo, oferta_id=oferta_id)
                
                # Convertir pretensión salarial
                pretension = None
                if pretension_salarial:
                    try:
                        pretension = Decimal(pretension_salarial)
                    except (InvalidOperation, ValueError):
                        messages.error(request, "Pretensión salarial inválida.")
                        return redirect('jobs:postular_trabajo', tipo=tipo, oferta_id=oferta_id)
                
                # Crear postulación
                resultado = self.service.crear_postulacion(
                    trabajador_id=usuario.id_usuario,
                    oferta_id=oferta_id,
                    tipo_oferta=tipo,
                    mensaje=mensaje,
                    pretension_salarial=pretension,
                    disponibilidad_inmediata=disponibilidad_inmediata
                )
                
                if resultado['success']:
                    messages.success(request, resultado['message'])
                    return redirect('jobs:mis_postulaciones')
                else:
                    messages.error(request, resultado['message'])
            
            # GET: Mostrar formulario
            context = {
                'oferta': oferta,
                'tipo': tipo,
                'usuario': usuario,
            }
            
            return render(request, 'jobs/postulaciones/postular.html', context)
            
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
            return redirect('users:login')
    
    @method_decorator(login_required)
    def mis_postulaciones(self, request):
        """Ver todas las postulaciones del trabajador"""
        try:
            usuario = Usuario.objects.get(user=request.user)
            
            # Obtener filtro de estado
            estado_filtro = request.GET.get('estado')
            
            # Obtener postulaciones
            postulaciones = self.service.get_postulaciones_trabajador(
                usuario.id_usuario,
                estado=estado_filtro
            )
            
            # Obtener estadísticas
            estadisticas = self.service.get_estadisticas_trabajador(usuario.id_usuario)
            
            context = {
                'postulaciones': postulaciones,
                'estadisticas': estadisticas,
                'estado_filtro': estado_filtro,
                'usuario': usuario,
            }
            
            return render(request, 'jobs/postulaciones/mis_postulaciones.html', context)
            
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
            return redirect('users:login')
    
    @method_decorator(login_required)
    @method_decorator(require_POST)
    def retirar_postulacion(self, request, postulacion_id):
        """Retirar una postulación"""
        try:
            usuario = Usuario.objects.get(user=request.user)
            
            resultado = self.service.retirar_postulacion(
                postulacion_id,
                usuario.id_usuario
            )
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse(resultado)
            
            if resultado['success']:
                messages.success(request, resultado['message'])
            else:
                messages.error(request, resultado['message'])
            
            return redirect('jobs:mis_postulaciones')
            
        except Usuario.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Usuario no encontrado'
            }, status=404)


# Instancia global
postulacion_views = PostulacionViews()