"""
Vistas de Gestión de Postulaciones 
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction

from apps.jobs.models import OfertaUsuario, OfertaEmpresa, Postulacion
from apps.jobs.utils import (
    obtener_postulaciones_usuario,
    obtener_postulaciones_empleador,
    formatear_postulacion,
    obtener_estadisticas_trabajador
)
from apps.users.models import Usuario


@login_required
def postular_trabajo(request, tipo, oferta_id):
    """
    Postular a una oferta de trabajo
    """
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        # Validar que sea trabajador
        if usuario.tipo_usuario not in ['trabajador', 'ambos']:
            messages.error(request, "Solo los trabajadores pueden postular.")
            return redirect('jobs:buscar_trabajos')
        
        # Obtener oferta según tipo
        if tipo == 'usuario':
            oferta = get_object_or_404(
                OfertaUsuario,
                id=oferta_id,
                estado='activa'
            )
            campo_oferta = 'id_oferta_usuario'
        elif tipo == 'empresa':
            oferta = get_object_or_404(
                OfertaEmpresa,
                id=oferta_id,
                estado='activa'
            )
            campo_oferta = 'id_oferta_empresa'
        else:
            messages.error(request, "Tipo de oferta inválido.")
            return redirect('jobs:buscar_trabajos')
        
        # Verificar que no sea el dueño
        if oferta.id_empleador.id_usuario == usuario.id_usuario:
            messages.error(request, "No puedes postular a tu propia oferta.")
            return redirect('jobs:detalle_trabajo', tipo=tipo, trabajo_id=oferta_id)
        
        # Verificar si ya postuló
        filtro = {
            'id_trabajador': usuario,
            campo_oferta: oferta
        }
        
        if Postulacion.objects.filter(**filtro).exists():
            messages.warning(request, "Ya postulaste a esta oferta.")
            return redirect('jobs:detalle_trabajo', tipo=tipo, trabajo_id=oferta_id)
        
        if request.method == 'POST':
            mensaje = request.POST.get('mensaje', '').strip()
            pretension_salarial = request.POST.get('pretension_salarial')
            disponibilidad_inmediata = request.POST.get('disponibilidad_inmediata') == 'on'
            
            # Validar mensaje
            if not mensaje:
                messages.error(request, "Debes incluir un mensaje de presentación.")
                return redirect('jobs:postular_trabajo', tipo=tipo, oferta_id=oferta_id)
            
            try:
                with transaction.atomic():
                    datos_postulacion = {
                        'id_trabajador': usuario,
                        campo_oferta: oferta,
                        'mensaje': mensaje,
                        'disponibilidad_inmediata': disponibilidad_inmediata,
                        'estado': 'pendiente'
                    }
                    
                    if pretension_salarial:
                        datos_postulacion['pretension_salarial'] = pretension_salarial
                    
                    Postulacion.objects.create(**datos_postulacion)
                
                messages.success(request, "✅ ¡Postulación enviada exitosamente!")
                return redirect('jobs:mis_postulaciones')
                
            except Exception as e:
                messages.error(request, f"Error al enviar postulación: {str(e)}")
        
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


@login_required
def mis_postulaciones(request):
    """
    Ver todas las postulaciones del trabajador
    """
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        # Obtener filtro de estado
        estado_filtro = request.GET.get('estado')
        
        # Obtener postulaciones
        postulaciones = obtener_postulaciones_usuario(usuario, estado=estado_filtro)
        
        # Formatear postulaciones
        postulaciones_data = [formatear_postulacion(p) for p in postulaciones]
        
        # Obtener estadísticas
        estadisticas = obtener_estadisticas_trabajador(usuario)
        
        context = {
            'postulaciones': postulaciones_data,
            'estadisticas': estadisticas,
            'estado_filtro': estado_filtro,
            'usuario': usuario,
        }
        
        return render(request, 'jobs/postulaciones/mis_postulaciones.html', context)
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')


@login_required
@require_POST
def retirar_postulacion(request, postulacion_id):
    """
    Retirar una postulación
    """
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        postulacion = get_object_or_404(
            Postulacion,
            id_postulacion=postulacion_id,
            id_trabajador=usuario
        )
        
        # Solo se puede retirar si está pendiente o en revisión
        if postulacion.estado not in ['pendiente', 'en_revision']:
            return JsonResponse({
                'success': False,
                'message': 'No puedes retirar esta postulación'
            }, status=400)
        
        # Eliminar postulación
        postulacion.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Postulación retirada correctamente'
        })
        
    except Usuario.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Usuario no encontrado'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@login_required
def ver_postulantes(request, tipo, oferta_id):
    """
    Ver postulantes de una oferta (solo para empleadores)
    """
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        # Obtener oferta
        if tipo == 'usuario':
            oferta = get_object_or_404(
                OfertaUsuario,
                id=oferta_id,
                id_empleador=usuario
            )
            postulaciones = oferta.postulaciones.all()
        elif tipo == 'empresa':
            oferta = get_object_or_404(
                OfertaEmpresa,
                id=oferta_id,
                id_empleador=usuario
            )
            postulaciones = oferta.postulaciones.all()
        else:
            messages.error(request, "Tipo de oferta inválido.")
            return redirect('jobs:mis_trabajos')
        
        # Obtener filtro de estado
        estado_filtro = request.GET.get('estado')
        if estado_filtro:
            postulaciones = postulaciones.filter(estado=estado_filtro)
        
        # Ordenar por fecha
        postulaciones = postulaciones.select_related(
            'id_trabajador',
            'id_trabajador__profile_detalle'
        ).order_by('-created_at')
        
        # Formatear postulaciones
        postulaciones_data = [formatear_postulacion(p) for p in postulaciones]
        
        context = {
            'oferta': oferta,
            'tipo': tipo,
            'postulaciones': postulaciones_data,
            'estado_filtro': estado_filtro,
            'total_postulaciones': len(postulaciones_data),
        }
        
        return render(request, 'jobs/postulaciones/ver_postulantes.html', context)
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')


@login_required
@require_POST
def aceptar_postulante(request, postulacion_id):
    """
    Aceptar una postulación
    """
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        postulacion = get_object_or_404(Postulacion, id_postulacion=postulacion_id)
        
        # Verificar que sea el dueño de la oferta
        oferta = postulacion.oferta
        if oferta.id_empleador.id_usuario != usuario.id_usuario:
            return JsonResponse({
                'success': False,
                'message': 'No tienes permisos para esta acción'
            }, status=403)
        
        # Cambiar estado
        postulacion.estado = 'aceptada'
        postulacion.save(update_fields=['estado', 'updated_at'])
        
        # TODO: Crear notificación para el trabajador
        
        return JsonResponse({
            'success': True,
            'message': 'Postulación aceptada correctamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@login_required
@require_POST
def rechazar_postulante(request, postulacion_id):
    """
    Rechazar una postulación
    """
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        postulacion = get_object_or_404(Postulacion, id_postulacion=postulacion_id)
        
        # Verificar que sea el dueño de la oferta
        oferta = postulacion.oferta
        if oferta.id_empleador.id_usuario != usuario.id_usuario:
            return JsonResponse({
                'success': False,
                'message': 'No tienes permisos para esta acción'
            }, status=403)
        
        # Cambiar estado
        postulacion.estado = 'rechazada'
        postulacion.save(update_fields=['estado', 'updated_at'])
        
        # TODO: Crear notificación para el trabajador
        
        return JsonResponse({
            'success': True,
            'message': 'Postulación rechazada'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)