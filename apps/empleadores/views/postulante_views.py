from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.jobs.models import Postulacion, OfertaUsuario, OfertaEmpresa
from apps.users.models import Usuario


@login_required
def ver_postulantes(request, oferta_id, tipo):
    """Ver postulantes de una oferta"""
    usuario = Usuario.objects.get(user=request.user)
    
    if tipo == 'usuario':
        oferta = get_object_or_404(OfertaUsuario, id=oferta_id, id_empleador=usuario)
        postulaciones = Postulacion.objects.filter(
            id_oferta_usuario=oferta
        ).select_related('id_trabajador')
    elif tipo == 'empresa':
        oferta = get_object_or_404(OfertaEmpresa, id=oferta_id, id_empleador=usuario)
        postulaciones = Postulacion.objects.filter(
            id_oferta_empresa=oferta
        ).select_related('id_trabajador')
    else:
        messages.error(request, "Tipo de oferta inválido.")
        return redirect('empleadores:listar_ofertas')
    
    context = {
        'oferta': oferta,
        'postulaciones': postulaciones,
        'tipo': tipo,
    }
    
    return render(request, 'empleadores/postulantes/ver.html', context)


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
    return redirect('empleadores:ver_postulantes', 
                    oferta_id=postulacion.id_oferta_usuario.id if postulacion.id_oferta_usuario else postulacion.id_oferta_empresa.id,
                    tipo='usuario' if postulacion.id_oferta_usuario else 'empresa')


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
    return redirect('empleadores:ver_postulantes',
                    oferta_id=postulacion.id_oferta_usuario.id if postulacion.id_oferta_usuario else postulacion.id_oferta_empresa.id,
                    tipo='usuario' if postulacion.id_oferta_usuario else 'empresa')