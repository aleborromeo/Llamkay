from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from apps.users.models import Usuario
from apps.empleadores.services import PostulanteService


postulante_service = PostulanteService()


@login_required
def ver_postulantes(request, oferta_id, tipo):
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        if tipo not in ['usuario', 'empresa']:
            messages.error(request, "Tipo de oferta inválido.")
            return redirect('empleadores:mis_trabajos')
        
        estado_filtro = request.GET.get('estado')
        
        resultado = postulante_service.get_postulantes_oferta(
            oferta_id,
            tipo,
            usuario.id_usuario,
            estado=estado_filtro
        )
        
        postulaciones = resultado['postulaciones']

        pendientes = postulaciones.filter(estado="pendiente").count()
        aceptadas = postulaciones.filter(estado="aceptada").count()
        rechazadas = postulaciones.filter(estado="rechazada").count()
        
        context = {
            'postulaciones': resultado['postulaciones'],
            'estadisticas': resultado['estadisticas'],
            'oferta_id': oferta_id,
            'tipo': tipo,
            'estado_filtro': estado_filtro,
            'usuario': usuario,
        }
        
        return render(request, 'empleadores/postulantes/ver.html', context)
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')


@login_required
@require_POST
def aceptar_postulante(request, postulacion_id):
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        resultado = postulante_service.aceptar_postulante(
            postulacion_id,
            usuario.id_usuario
        )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(resultado)
        
        if resultado['success']:
            messages.success(request, resultado['message'])
        else:
            messages.error(request, resultado['message'])
        
        return redirect(request.META.get('HTTP_REFERER', 'empleadores:mis_trabajos'))
        
    except Usuario.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Usuario no encontrado'
        }, status=404)


@login_required
@require_POST
def rechazar_postulante(request, postulacion_id):
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        resultado = postulante_service.rechazar_postulante(
            postulacion_id,
            usuario.id_usuario
        )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse(resultado)
        
        if resultado['success']:
            messages.success(request, resultado['message'])
        else:
            messages.error(request, resultado['message'])
        
        return redirect(request.META.get('HTTP_REFERER', 'empleadores:mis_trabajos'))
        
    except Usuario.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Usuario no encontrado'
        }, status=404)


@login_required
def postulaciones_recientes(request):
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        postulaciones = postulante_service.get_postulaciones_recientes(
            usuario.id_usuario,
            limit=10
        )
        
        return JsonResponse({
            'success': True,
            'postulaciones': postulaciones
        })
        
    except Usuario.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Usuario no encontrado'
        }, status=404)