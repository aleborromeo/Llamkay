"""
Vistas de Calificación - REFACTORIZADAS
Responsabilidad: Solo manejar request/response
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from apps.users.services import CalificacionService
from apps.users.repositories import UsuarioRepository
from apps.users.models import Usuario
from apps.jobs.models import Contrato


@login_required
def calificar_usuario(request, usuario_id):
    """
    Vista para calificar a un usuario después de un contrato
    """
    usuario_repo = UsuarioRepository()
    
    try:
        usuario_actual = usuario_repo.obtener_por_user(request.user)
        if not usuario_actual:
            messages.error(request, 'Debes completar tu perfil primero.')
            return redirect('users:perfil')
    except Exception:
        messages.error(request, 'Error al obtener tu perfil.')
        return redirect('users:perfil')
    
    usuario_calificado = get_object_or_404(Usuario, id_usuario=usuario_id)
    
    if request.method == 'POST':
        calificacion_service = CalificacionService()
        
        # Preparar datos
        try:
            datos = {
                'puntuacion': int(request.POST.get('puntuacion')),
                'comentario': request.POST.get('comentario', '').strip(),
                'puntualidad': int(request.POST.get('puntualidad')) if request.POST.get('puntualidad') else None,
                'calidad_trabajo': int(request.POST.get('calidad_trabajo')) if request.POST.get('calidad_trabajo') else None,
                'comunicacion': int(request.POST.get('comunicacion')) if request.POST.get('comunicacion') else None,
            }
            
            # Validar rango
            if not (1 <= datos['puntuacion'] <= 5):
                raise ValueError("Puntuación fuera de rango")
            
        except (ValueError, TypeError) as e:
            messages.error(request, f'Puntuación inválida: {str(e)}')
            return redirect('users:calificar_usuario', usuario_id=usuario_id)
        
        # Buscar contrato (simplificado - deberías pasarlo como parámetro)
        contrato = Contrato.objects.filter(
            id_empleador=usuario_actual,
            id_trabajador=usuario_calificado,
            estado='completado'
        ).first() or Contrato.objects.filter(
            id_empleador=usuario_calificado,
            id_trabajador=usuario_actual,
            estado='completado'
        ).first()
        
        # Crear calificación usando el servicio
        resultado = calificacion_service.crear_calificacion(
            autor=usuario_actual,
            receptor=usuario_calificado,
            contrato=contrato,
            datos=datos
        )
        
        if resultado['success']:
            messages.success(request, resultado['message'])
            return redirect('users:ver_calificaciones', usuario_id=usuario_calificado.id_usuario)
        else:
            messages.error(request, resultado['error'])
    
    # GET: Mostrar formulario
    return render(request, 'users/calificar.html', {
        'usuario_calificado': usuario_calificado,
    })


@login_required
def ver_calificaciones(request, usuario_id):
    """
    Ver todas las calificaciones de un usuario
    """
    calificacion_service = CalificacionService()
    
    resultado = calificacion_service.obtener_calificaciones_usuario(usuario_id)
    
    if not resultado['success']:
        messages.error(request, resultado['error'])
        return redirect('llamkay:dashboard')
    
    return render(request, 'users/ver_calificaciones.html', resultado)


@login_required
@require_POST
def eliminar_calificacion(request, calificacion_id):
    """
    Desactivar una calificación (solo el autor puede desactivarla)
    """
    usuario_repo = UsuarioRepository()
    
    try:
        usuario_actual = usuario_repo.obtener_por_user(request.user)
        if not usuario_actual:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=400)
    except Exception:
        return JsonResponse({'error': 'Error al obtener usuario'}, status=500)
    
    calificacion_service = CalificacionService()
    resultado = calificacion_service.eliminar_calificacion(calificacion_id, usuario_actual)
    
    if resultado['success']:
        return JsonResponse({
            'success': True,
            'message': resultado['message']
        })
    else:
        return JsonResponse({
            'error': resultado['error']
        }, status=400)


@login_required
def mis_calificaciones(request):
    """
    Ver las calificaciones que el usuario ha dado y recibido
    """
    usuario_repo = UsuarioRepository()
    
    try:
        usuario_actual = usuario_repo.obtener_por_user(request.user)
        if not usuario_actual:
            messages.error(request, 'Debes completar tu perfil primero.')
            return redirect('users:perfil')
    except Exception:
        messages.error(request, 'Error al obtener tu perfil.')
        return redirect('users:perfil')
    
    calificacion_service = CalificacionService()
    resultado = calificacion_service.obtener_mis_calificaciones(usuario_actual)
    
    return render(request, 'users/mis_calificaciones.html', resultado)


def buscar_usuarios(request):
    """
    Buscar usuarios por nombre, habilidades o ubicación
    """
    query = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', '')
    
    usuario_repo = UsuarioRepository()
    usuarios = usuario_repo.buscar(query, tipo)
    
    context = {
        'usuarios': usuarios,
        'query': query,
        'tipo': tipo,
    }
    
    return render(request, 'users/buscar_usuarios.html', context)