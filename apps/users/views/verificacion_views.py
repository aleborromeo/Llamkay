"""
Vistas de Verificación - REFACTORIZADAS
Responsabilidad: Solo manejar request/response
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from apps.users.services import VerificacionService
from apps.users.repositories import UsuarioRepository
from apps.users.forms import CertificacionForm, VerificacionForm


@login_required
def solicitar_verificacion(request):
    """
    Solicitar verificación de identidad
    """
    usuario_repo = UsuarioRepository()
    
    try:
        usuario = usuario_repo.obtener_por_user(request.user)
        if not usuario:
            messages.error(request, 'Usuario no encontrado.')
            return redirect('users:perfil')
    except Exception:
        messages.error(request, 'Error al obtener usuario.')
        return redirect('users:perfil')
    
    if request.method == 'POST':
        form = VerificacionForm(request.POST, request.FILES)
        
        if form.is_valid():
            verificacion_service = VerificacionService()
            
            tipo = form.cleaned_data['tipo']
            observaciones = form.cleaned_data.get('observaciones', '')
            
            # Preparar archivos según el tipo
            archivos = {}
            if tipo == 'dni':
                archivos['frontal'] = request.FILES.get('archivo_frontal')
                archivos['posterior'] = request.FILES.get('archivo_posterior')
            else:
                archivos['archivo'] = request.FILES.get('archivo_url')
            
            # Solicitar verificación usando el servicio
            resultado = verificacion_service.solicitar_verificacion(
                usuario=usuario,
                tipo=tipo,
                archivos=archivos,
                observaciones=observaciones
            )
            
            if resultado['success']:
                messages.success(request, resultado['message'])
                return redirect('users:perfil')
            else:
                messages.error(request, resultado['error'])
    else:
        form = VerificacionForm()
    
    return render(request, 'users/verificacion/solicitar.html', {
        'form': form,
        'usuario': usuario
    })


@login_required
def subir_certificacion(request):
    """
    Subir certificación profesional
    """
    usuario_repo = UsuarioRepository()
    
    try:
        usuario = usuario_repo.obtener_por_user(request.user)
        if not usuario:
            messages.error(request, 'Usuario no encontrado.')
            return redirect('users:perfil')
    except Exception:
        messages.error(request, 'Error al obtener usuario.')
        return redirect('users:perfil')
    
    if request.method == 'POST':
        form = CertificacionForm(request.POST, request.FILES)
        
        if form.is_valid():
            verificacion_service = VerificacionService()
            
            # Subir certificación usando el servicio
            resultado = verificacion_service.subir_certificacion(
                usuario=usuario,
                titulo=form.cleaned_data['titulo'],
                institucion=form.cleaned_data.get('institucion'),
                descripcion=form.cleaned_data.get('descripcion'),
                archivo=form.cleaned_data.get('archivo'),
                fecha_obtencion=form.cleaned_data.get('fecha_obtencion'),
                fecha_expiracion=form.cleaned_data.get('fecha_expiracion')
            )
            
            if resultado['success']:
                messages.success(request, resultado['message'])
                return redirect('users:perfil')
            else:
                messages.error(request, resultado['error'])
    else:
        form = CertificacionForm()
    
    return render(request, 'users/verificacion/certificacion.html', {
        'form': form,
        'usuario': usuario
    })


@login_required
def mis_verificaciones(request):
    """
    Ver el estado de todas las verificaciones del usuario
    """
    usuario_repo = UsuarioRepository()
    
    try:
        usuario = usuario_repo.obtener_por_user(request.user)
        if not usuario:
            messages.error(request, 'Usuario no encontrado.')
            return redirect('users:perfil')
    except Exception:
        messages.error(request, 'Error al obtener usuario.')
        return redirect('users:perfil')
    
    verificacion_service = VerificacionService()
    
    # Obtener verificaciones y estado
    verificaciones = verificacion_service.listar_verificaciones_usuario(usuario)
    estados = verificacion_service.obtener_estado_verificacion(usuario)
    certificaciones = verificacion_service.listar_certificaciones_usuario(usuario)
    
    context = {
        'usuario': usuario,
        'verificaciones': verificaciones,
        'estados': estados,
        'certificaciones': certificaciones,
    }
    
    return render(request, 'users/verificacion/mis_verificaciones.html', context)


@login_required
def mis_certificaciones(request):
    """
    Ver todas las certificaciones del usuario
    """
    usuario_repo = UsuarioRepository()
    
    try:
        usuario = usuario_repo.obtener_por_user(request.user)
        if not usuario:
            messages.error(request, 'Usuario no encontrado.')
            return redirect('users:perfil')
    except Exception:
        messages.error(request, 'Error al obtener usuario.')
        return redirect('users:perfil')
    
    verificacion_service = VerificacionService()
    certificaciones = verificacion_service.listar_certificaciones_usuario(usuario)
    
    context = {
        'usuario': usuario,
        'certificaciones': certificaciones,
    }
    
    return render(request, 'users/verificacion/mis_certificaciones.html', context)