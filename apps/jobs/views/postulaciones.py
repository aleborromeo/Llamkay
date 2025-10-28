from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from django.core.exceptions import PermissionDenied

from apps.jobs.models import OfertaUsuario, OfertaEmpresa, Postulacion
from apps.users.models import Usuario


@login_required
def postular_trabajo(request, tipo, oferta_id):
    """Postular a una oferta de trabajo"""
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        # Verificar que el usuario sea trabajador
        # ✅ Asumiendo que Usuario tiene campo 'tipo_usuario'
        # Si no existe, comentar esta validación
        # if hasattr(usuario, 'tipo_usuario') and usuario.tipo_usuario not in ['trabajador', 'ambos']:
        #     messages.error(request, "Solo los trabajadores pueden postular.")
        #     return redirect('jobs:buscar_trabajos')
        
        if tipo == 'usuario':
            oferta = get_object_or_404(OfertaUsuario, id=oferta_id, estado='activa')
            
            # Verificar que no sea el dueño
            if oferta.id_empleador == usuario:
                messages.error(request, "No puedes postular a tu propia oferta.")
                return redirect('jobs:detalle_trabajo', tipo=tipo, trabajo_id=oferta_id)
            
            # Verificar si ya postuló
            ya_postulo = Postulacion.objects.filter(
                id_trabajador=usuario,
                id_oferta_usuario=oferta
            ).exists()
            
            if ya_postulo:
                messages.warning(request, "Ya postulaste a esta oferta.")
                return redirect('jobs:detalle_trabajo', tipo=tipo, trabajo_id=oferta_id)
            
            if request.method == 'POST':
                mensaje = request.POST.get('mensaje', '').strip()
                pretension_salarial = request.POST.get('pretension_salarial')
                disponibilidad_inmediata = request.POST.get('disponibilidad_inmediata') == 'on'
                
                with transaction.atomic():
                    Postulacion.objects.create(
                        id_trabajador=usuario,
                        id_oferta_usuario=oferta,
                        mensaje=mensaje,
                        pretension_salarial=pretension_salarial if pretension_salarial else None,
                        disponibilidad_inmediata=disponibilidad_inmediata
                    )
                
                messages.success(request, "¡Postulación enviada exitosamente!")
                return redirect('jobs:mis_postulaciones')
                
        elif tipo == 'empresa':
            oferta = get_object_or_404(OfertaEmpresa, id=oferta_id, estado='activa')
            
            if oferta.id_empleador == usuario:
                messages.error(request, "No puedes postular a tu propia oferta.")
                return redirect('jobs:detalle_trabajo', tipo=tipo, trabajo_id=oferta_id)
            
            ya_postulo = Postulacion.objects.filter(
                id_trabajador=usuario,
                id_oferta_empresa=oferta
            ).exists()
            
            if ya_postulo:
                messages.warning(request, "Ya postulaste a esta oferta.")
                return redirect('jobs:detalle_trabajo', tipo=tipo, trabajo_id=oferta_id)
            
            if request.method == 'POST':
                mensaje = request.POST.get('mensaje', '').strip()
                pretension_salarial = request.POST.get('pretension_salarial')
                disponibilidad_inmediata = request.POST.get('disponibilidad_inmediata') == 'on'
                
                with transaction.atomic():
                    Postulacion.objects.create(
                        id_trabajador=usuario,
                        id_oferta_empresa=oferta,
                        mensaje=mensaje,
                        pretension_salarial=pretension_salarial if pretension_salarial else None,
                        disponibilidad_inmediata=disponibilidad_inmediata
                    )
                
                messages.success(request, "¡Postulación enviada exitosamente!")
                return redirect('jobs:mis_postulaciones')
        else:
            messages.error(request, "Tipo de oferta inválido.")
            return redirect('jobs:buscar_trabajos')
        
        context = {
            'oferta': oferta,
            'tipo': tipo,
        }
        
        return render(request, 'jobs/postulaciones/postular.html', context)
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')


@login_required
def mis_postulaciones(request):
    """Ver todas las postulaciones del trabajador"""
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        postulaciones = Postulacion.objects.filter(
            id_trabajador=usuario
        ).select_related(
            'id_oferta_usuario',
            'id_oferta_empresa',
            'id_oferta_usuario__id_empleador',
            'id_oferta_empresa__id_empleador'
        ).order_by('-created_at')  # ✅ Cambiado de fecha_postulacion
        
        postulaciones_data = []
        for post in postulaciones:
            if post.id_oferta_usuario:
                oferta = post.id_oferta_usuario
                postulaciones_data.append({
                    'id': post.id_postulacion,
                    'tipo': 'usuario',
                    'titulo': oferta.titulo,
                    'empleador': oferta.id_empleador,
                    'estado': post.estado,
                    'fecha_postulacion': post.created_at,  # ✅ Cambiado
                    'leida': post.leida,
                    'mensaje': post.mensaje,
                })
            elif post.id_oferta_empresa:
                oferta = post.id_oferta_empresa
                postulaciones_data.append({
                    'id': post.id_postulacion,
                    'tipo': 'empresa',
                    'titulo': oferta.titulo_puesto,
                    'empleador': oferta.id_empleador,
                    'estado': post.estado,
                    'fecha_postulacion': post.created_at,  # ✅ Cambiado
                    'leida': post.leida,
                    'mensaje': post.mensaje,
                })
        
        context = {
            'postulaciones': postulaciones_data,
        }
        
        return render(request, 'jobs/postulaciones/mis_postulaciones.html', context)
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')


@login_required
@require_POST
def retirar_postulacion(request, postulacion_id):
    """Retirar una postulación"""
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
        
        # ✅ Cambiado: El modelo no tiene estado 'retirada', usar 'rechazada' o eliminarlo
        postulacion.delete()  # O cambiar estado si prefieres soft delete
        
        return JsonResponse({
            'success': True,
            'message': 'Postulación retirada correctamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@login_required
def aceptar_postulante(request, postulacion_id):
    """Aceptar una postulación"""
    postulacion = get_object_or_404(Postulacion, id_postulacion=postulacion_id)
    
    # Verificar que el usuario sea el dueño de la oferta
    usuario = Usuario.objects.get(user=request.user)
    
    if postulacion.id_oferta_usuario:
        if postulacion.id_oferta_usuario.id_empleador != usuario:
            raise PermissionDenied
    elif postulacion.id_oferta_empresa:
        if postulacion.id_oferta_empresa.id_empleador != usuario:
            raise PermissionDenied
    
    postulacion.estado = 'aceptada'
    postulacion.save()
    
    messages.success(request, "Postulación aceptada correctamente.")
    
    # Redirigir según tipo
    if postulacion.id_oferta_usuario:
        return redirect('empleadores:ver_postulantes', 
                       oferta_id=postulacion.id_oferta_usuario.id,
                       tipo='usuario')
    else:
        return redirect('empleadores:ver_postulantes',
                       oferta_id=postulacion.id_oferta_empresa.id,
                       tipo='empresa')


@login_required
def rechazar_postulante(request, postulacion_id):
    """Rechazar una postulación"""
    postulacion = get_object_or_404(Postulacion, id_postulacion=postulacion_id)
    
    # Verificar permisos
    usuario = Usuario.objects.get(user=request.user)
    
    if postulacion.id_oferta_usuario:
        if postulacion.id_oferta_usuario.id_empleador != usuario:
            raise PermissionDenied
    elif postulacion.id_oferta_empresa:
        if postulacion.id_oferta_empresa.id_empleador != usuario:
            raise PermissionDenied
    
    postulacion.estado = 'rechazada'
    postulacion.save()
    
    messages.success(request, "Postulación rechazada.")
    
    # Redirigir según tipo
    if postulacion.id_oferta_usuario:
        return redirect('empleadores:ver_postulantes',
                       oferta_id=postulacion.id_oferta_usuario.id,
                       tipo='usuario')
    else:
        return redirect('empleadores:ver_postulantes',
                       oferta_id=postulacion.id_oferta_empresa.id,
                       tipo='empresa')