from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q

from apps.users.models import Usuario
from apps.jobs.models import Contrato, Calificacion  # Importar desde jobs


@login_required
def calificar_usuario(request, usuario_id):
    """Vista para calificar a un usuario después de un contrato"""
    try:
        usuario_actual = request.user.perfil
    except Usuario.DoesNotExist:
        messages.error(request, 'Debes completar tu perfil primero.')
        return redirect('users:perfil')
    
    usuario_calificado = get_object_or_404(Usuario, id_usuario=usuario_id)
    
    # Verificar que no sea el mismo usuario
    if usuario_actual.id_usuario == usuario_calificado.id_usuario:
        messages.error(request, 'No puedes calificarte a ti mismo.')
        return redirect('users:perfil')
    
    # Verificar que existe un contrato completado entre ambos usuarios
    contrato = Contrato.objects.filter(
        Q(id_empleador=usuario_actual, id_trabajador=usuario_calificado) |
        Q(id_empleador=usuario_calificado, id_trabajador=usuario_actual),
        estado='completado'
    ).first()
    
    if not contrato:
        messages.error(request, 'No tienes un contrato completado con este usuario.')
        return redirect('users:perfil')
    
    # Determinar el rol del autor
    if contrato.id_empleador.id_usuario == usuario_actual.id_usuario:
        rol_autor = 'empleador'
    else:
        rol_autor = 'trabajador'
    
    # Verificar si ya calificó en este contrato
    calificacion_existente = Calificacion.objects.filter(
        id_contrato=contrato,
        id_autor=usuario_actual
    ).first()
    
    if request.method == 'POST':
        puntuacion = request.POST.get('puntuacion')
        comentario = request.POST.get('comentario', '').strip()
        puntualidad = request.POST.get('puntualidad')
        calidad_trabajo = request.POST.get('calidad_trabajo')
        comunicacion = request.POST.get('comunicacion')
        
        if not puntuacion:
            messages.error(request, 'Debes seleccionar una puntuación.')
            return render(request, 'users/calificar.html', {
                'usuario_calificado': usuario_calificado,
                'calificacion_existente': calificacion_existente,
                'contrato': contrato
            })
        
        try:
            puntuacion = int(puntuacion)
            if puntuacion < 1 or puntuacion > 5:
                raise ValueError("Puntuación fuera de rango")
            
            # Validar puntuaciones detalladas si fueron enviadas
            if puntualidad:
                puntualidad = int(puntualidad)
                if puntualidad < 1 or puntualidad > 5:
                    raise ValueError("Puntualidad fuera de rango")
            else:
                puntualidad = None
                
            if calidad_trabajo:
                calidad_trabajo = int(calidad_trabajo)
                if calidad_trabajo < 1 or calidad_trabajo > 5:
                    raise ValueError("Calidad fuera de rango")
            else:
                calidad_trabajo = None
                
            if comunicacion:
                comunicacion = int(comunicacion)
                if comunicacion < 1 or comunicacion > 5:
                    raise ValueError("Comunicación fuera de rango")
            else:
                comunicacion = None
                
        except (ValueError, TypeError) as e:
            messages.error(request, f'Puntuación inválida: {str(e)}')
            return render(request, 'users/calificar.html', {
                'usuario_calificado': usuario_calificado,
                'calificacion_existente': calificacion_existente,
                'contrato': contrato
            })
        
        if calificacion_existente:
            # Actualizar calificación existente
            calificacion_existente.puntuacion = puntuacion
            calificacion_existente.comentario = comentario
            calificacion_existente.puntualidad = puntualidad
            calificacion_existente.calidad_trabajo = calidad_trabajo
            calificacion_existente.comunicacion = comunicacion
            calificacion_existente.editada = True
            calificacion_existente.save()
            messages.success(request, 'Calificación actualizada correctamente.')
        else:
            # Crear nueva calificación
            Calificacion.objects.create(
                id_contrato=contrato,
                id_autor=usuario_actual,
                id_receptor=usuario_calificado,
                rol_autor=rol_autor,
                puntuacion=puntuacion,
                comentario=comentario,
                puntualidad=puntualidad,
                calidad_trabajo=calidad_trabajo,
                comunicacion=comunicacion
            )
            messages.success(request, 'Calificación enviada correctamente.')
        
        # Actualizar estadísticas del usuario calificado
        actualizar_estadisticas_usuario(usuario_calificado)
        
        return redirect('users:ver_calificaciones', usuario_id=usuario_calificado.id_usuario)
    
    return render(request, 'users/calificar.html', {
        'usuario_calificado': usuario_calificado,
        'calificacion_existente': calificacion_existente,
        'contrato': contrato,
        'rol_autor': rol_autor
    })


@login_required
def ver_calificaciones(request, usuario_id):
    """Ver todas las calificaciones de un usuario"""
    usuario = get_object_or_404(Usuario, id_usuario=usuario_id)
    
    calificaciones = Calificacion.objects.filter(
        id_receptor=usuario,
        activa=True
    ).select_related('id_autor', 'id_contrato').order_by('-fecha')
    
    # Calcular estadísticas
    total = calificaciones.count()
    promedio = usuario.rating_promedio
    
    # Contar por estrellas
    estrellas = {i: 0 for i in range(1, 6)}
    for cal in calificaciones:
        estrellas[cal.puntuacion] += 1
    
    # Calcular promedios de aspectos detallados
    calificaciones_con_detalles = calificaciones.exclude(
        puntualidad__isnull=True,
        calidad_trabajo__isnull=True,
        comunicacion__isnull=True
    )
    
    promedio_puntualidad = None
    promedio_calidad = None
    promedio_comunicacion = None
    
    if calificaciones_con_detalles.exists():
        from django.db.models import Avg
        promedios = calificaciones_con_detalles.aggregate(
            Avg('puntualidad'),
            Avg('calidad_trabajo'),
            Avg('comunicacion')
        )
        promedio_puntualidad = round(promedios['puntualidad__avg'], 1) if promedios['puntualidad__avg'] else None
        promedio_calidad = round(promedios['calidad_trabajo__avg'], 1) if promedios['calidad_trabajo__avg'] else None
        promedio_comunicacion = round(promedios['comunicacion__avg'], 1) if promedios['comunicacion__avg'] else None
    
    context = {
        'usuario': usuario,
        'calificaciones': calificaciones,
        'total_calificaciones': total,
        'promedio': promedio,
        'estrellas': estrellas,
        'promedio_puntualidad': promedio_puntualidad,
        'promedio_calidad': promedio_calidad,
        'promedio_comunicacion': promedio_comunicacion,
    }
    
    return render(request, 'users/ver_calificaciones.html', context)


@login_required
@require_POST
def eliminar_calificacion(request, calificacion_id):
    """Desactivar una calificación (solo el autor puede desactivarla)"""
    try:
        usuario_actual = request.user.perfil
    except Usuario.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=400)
    
    try:
        calificacion = get_object_or_404(
            Calificacion, 
            id_calificacion=calificacion_id, 
            id_autor=usuario_actual
        )
        
        usuario_calificado = calificacion.id_receptor
        
        # Marcar como inactiva en lugar de eliminar
        calificacion.activa = False
        calificacion.save(update_fields=['activa'])
        
        # Actualizar estadísticas
        actualizar_estadisticas_usuario(usuario_calificado)
        
        return JsonResponse({
            'success': True, 
            'message': 'Calificación eliminada correctamente'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def mis_calificaciones(request):
    """Ver las calificaciones que el usuario ha dado y recibido"""
    try:
        usuario_actual = request.user.perfil
    except Usuario.DoesNotExist:
        messages.error(request, 'Debes completar tu perfil primero.')
        return redirect('users:perfil')
    
    # Calificaciones recibidas
    calificaciones_recibidas = Calificacion.objects.filter(
        id_receptor=usuario_actual,
        activa=True
    ).select_related('id_autor', 'id_contrato').order_by('-fecha')
    
    # Calificaciones dadas
    calificaciones_dadas = Calificacion.objects.filter(
        id_autor=usuario_actual,
        activa=True
    ).select_related('id_receptor', 'id_contrato').order_by('-fecha')
    
    context = {
        'calificaciones_recibidas': calificaciones_recibidas,
        'calificaciones_dadas': calificaciones_dadas,
        'usuario': usuario_actual,
    }
    
    return render(request, 'users/mis_calificaciones.html', context)


def buscar_usuarios(request):
    """Buscar usuarios por nombre, habilidades o ubicación"""
    query = request.GET.get('q', '').strip()
    tipo = request.GET.get('tipo', '')
    
    usuarios = Usuario.objects.filter(
        habilitado=True,
        deleted_at__isnull=True
    )
    
    if tipo and tipo != 'todos':
        usuarios = usuarios.filter(tipo_usuario=tipo)
    
    if query:
        usuarios = usuarios.filter(
            Q(nombres__icontains=query) |
            Q(apellidos__icontains=query) |
            Q(username__icontains=query)
        )
    
    # Ordenar por rating
    usuarios = usuarios.order_by('-rating_promedio', '-total_calificaciones')[:20]
    
    context = {
        'usuarios': usuarios,
        'query': query,
        'tipo': tipo,
    }
    
    return render(request, 'users/buscar_usuarios.html', context)


def actualizar_estadisticas_usuario(usuario):
    """Actualizar estadísticas de calificaciones de un usuario"""
    calificaciones = Calificacion.objects.filter(
        id_receptor=usuario,
        activa=True
    )
    
    total = calificaciones.count()
    
    if total > 0:
        suma = sum(cal.puntuacion for cal in calificaciones)
        promedio = suma / total
        
        usuario.total_calificaciones = total