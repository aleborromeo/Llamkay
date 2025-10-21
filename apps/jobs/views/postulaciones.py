from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction

from apps.jobs.models import (
    OfertaUsuario, OfertaEmpresa, Postulacion
)
from apps.users.models import Usuario


@login_required
def postular_trabajo(request, tipo, oferta_id):
    """Postular a una oferta de trabajo"""
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        # Verificar que el usuario sea trabajador
        if usuario.tipo_usuario not in ['trabajador', 'ambos']:
            messages.error(request, "Solo los trabajadores pueden postular.")
            return redirect('jobs:buscar_trabajos')
        
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
                cv_adjunto = request.FILES.get('cv_adjunto')
                
                with transaction.atomic():
                    Postulacion.objects.create(
                        id_trabajador=usuario,
                        id_oferta_usuario=oferta,
                        mensaje=mensaje,
                        pretension_salarial=pretension_salarial if pretension_salarial else None,
                        disponibilidad_inmediata=disponibilidad_inmediata,
                        cv_adjunto=cv_adjunto
                    )
                    
                    # Incrementar contador de postulaciones
                    oferta.postulaciones_count += 1
                    oferta.save(update_fields=['postulaciones_count'])
                
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
                cv_adjunto = request.FILES.get('cv_adjunto')
                
                with transaction.atomic():
                    Postulacion.objects.create(
                        id_trabajador=usuario,
                        id_oferta_empresa=oferta,
                        mensaje=mensaje,
                        pretension_salarial=pretension_salarial if pretension_salarial else None,
                        disponibilidad_inmediata=disponibilidad_inmediata,
                        cv_adjunto=cv_adjunto
                    )
                    
                    oferta.postulaciones_count += 1
                    oferta.save(update_fields=['postulaciones_count'])
                
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
            'id_oferta_empresa'
        ).order_by('-fecha_postulacion')
        
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
                    'fecha_postulacion': post.fecha_postulacion,
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
                    'fecha_postulacion': post.fecha_postulacion,
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
        
        postulacion.estado = 'retirada'
        postulacion.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Postulación retirada correctamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)