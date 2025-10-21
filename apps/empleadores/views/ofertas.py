from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from apps.jobs.models import OfertaUsuario, OfertaEmpresa
from apps.users.models import Usuario


@login_required
def crear_oferta(request):
    """Crear nueva oferta de trabajo"""
    usuario = Usuario.objects.get(user=request.user)
    
    # Determinar tipo de oferta según tipo de usuario
    if usuario.tipo_usuario == 'empresa':
        # Redirigir a formulario de empresa
        return redirect('empleadores:crear_oferta_empresa')
    else:
        # Formulario de usuario individual
        return redirect('empleadores:crear_oferta_individual')


@login_required
def listar_ofertas(request):
    """Listar todas las ofertas del empleador"""
    usuario = Usuario.objects.get(user=request.user)
    
    ofertas_usuario = OfertaUsuario.objects.filter(id_empleador=usuario)
    ofertas_empresa = OfertaEmpresa.objects.filter(id_empleador=usuario)
    
    context = {
        'ofertas_usuario': ofertas_usuario,
        'ofertas_empresa': ofertas_empresa,
    }
    
    return render(request, 'empleadores/ofertas/listar.html', context)


@login_required
def editar_oferta(request, oferta_id, tipo):
    """Editar oferta existente"""
    usuario = Usuario.objects.get(user=request.user)
    
    if tipo == 'usuario':
        oferta = get_object_or_404(OfertaUsuario, id=oferta_id, id_empleador=usuario)
    elif tipo == 'empresa':
        oferta = get_object_or_404(OfertaEmpresa, id=oferta_id, id_empleador=usuario)
    else:
        raise PermissionDenied
    
    if request.method == 'POST':
        # Procesar formulario
        # ...
        messages.success(request, "Oferta actualizada correctamente.")
        return redirect('empleadores:listar_ofertas')
    
    context = {
        'oferta': oferta,
        'tipo': tipo,
    }
    
    return render(request, 'empleadores/ofertas/editar.html', context)


@login_required
def eliminar_oferta(request, oferta_id, tipo):
    """Eliminar oferta"""
    usuario = Usuario.objects.get(user=request.user)
    
    if tipo == 'usuario':
        oferta = get_object_or_404(OfertaUsuario, id=oferta_id, id_empleador=usuario)
    elif tipo == 'empresa':
        oferta = get_object_or_404(OfertaEmpresa, id=oferta_id, id_empleador=usuario)
    else:
        raise PermissionDenied
    
    if request.method == 'POST':
        oferta.delete()
        messages.success(request, "Oferta eliminada correctamente.")
        return redirect('empleadores:listar_ofertas')
    
    return render(request, 'empleadores/ofertas/confirmar_eliminar.html', {
        'oferta': oferta
    })