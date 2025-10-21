from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from apps.users.models import Usuario, Verificacion, Certificacion


@login_required
def solicitar_verificacion(request):
    """Solicitar verificación de identidad"""
    if request.method == 'POST':
        tipo_verificacion = request.POST.get('tipo')
        archivo = request.FILES.get('archivo')
        
        if not archivo:
            messages.error(request, "Debes subir un archivo.")
            return redirect('users:perfil')
        
        usuario = Usuario.objects.get(user=request.user)
        
        Verificacion.objects.create(
            id_usuario=usuario,
            tipo=tipo_verificacion,
            archivo_url=archivo,
            estado='pendiente'
        )
        
        messages.success(request, "Solicitud enviada. Será revisada pronto.")
        return redirect('users:perfil')
    
    return render(request, 'users/verificacion/solicitar.html')


@login_required
def subir_certificacion(request):
    """Subir certificación profesional"""
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        institucion = request.POST.get('institucion')
        archivo = request.FILES.get('archivo')
        
        if not titulo or not archivo:
            messages.error(request, "Título y archivo son obligatorios.")
            return redirect('users:perfil')
        
        usuario = Usuario.objects.get(user=request.user)
        
        Certificacion.objects.create(
            id_usuario=usuario,
            titulo=titulo,
            institucion=institucion,
            archivo=archivo
        )
        
        messages.success(request, "Certificación subida correctamente.")
        return redirect('users:perfil')
    
    return render(request, 'users/verificacion/certificacion.html')