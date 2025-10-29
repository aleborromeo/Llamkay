"""
Vistas de Gestión de Trabajos Guardados
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction

from apps.jobs.models import OfertaUsuario, OfertaEmpresa, GuardarTrabajo
from apps.users.models import Usuario


@login_required
def trabajos_guardados(request):
    """
    Lista de trabajos guardados por el usuario
    """
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        # Obtener trabajos guardados con relaciones
        guardados = GuardarTrabajo.objects.filter(
            id_usuario=usuario
        ).select_related(
            'id_oferta_usuario',
            'id_oferta_usuario__id_empleador',
            'id_oferta_usuario__id_categoria',
            'id_oferta_usuario__id_departamento',
            'id_oferta_usuario__id_provincia',
            'id_oferta_usuario__id_distrito',
            'id_oferta_empresa',
            'id_oferta_empresa__id_empleador',
            'id_oferta_empresa__id_categoria',
            'id_oferta_empresa__id_departamento',
            'id_oferta_empresa__id_provincia',
            'id_oferta_empresa__id_distrito',
        ).order_by('-created_at')
        
        # Formatear trabajos
        trabajos = []
        for guardado in guardados:
            if guardado.id_oferta_usuario:
                oferta = guardado.id_oferta_usuario
                trabajos.append({
                    'guardado_id': guardado.id,
                    'tipo': 'usuario',
                    'id': oferta.id,
                    'titulo': oferta.titulo,
                    'descripcion': oferta.descripcion,
                    'pago': oferta.pago,
                    'moneda': oferta.moneda,
                    'modalidad_pago': oferta.get_modalidad_pago_display(),
                    'fecha_guardado': guardado.created_at,
                    'fecha_publicacion': oferta.created_at,
                    'estado': oferta.estado,
                    'empleador': {
                        'id': oferta.id_empleador.id_usuario,
                        'nombre': oferta.id_empleador.nombre_completo,
                    },
                    'ubicacion': {
                        'departamento': oferta.id_departamento.nombre if oferta.id_departamento else None,
                        'provincia': oferta.id_provincia.nombre if oferta.id_provincia else None,
                        'distrito': oferta.id_distrito.nombre if oferta.id_distrito else None,
                    },
                    'categoria': {
                        'nombre': oferta.id_categoria.nombre if oferta.id_categoria else None,
                    },
                })
            elif guardado.id_oferta_empresa:
                oferta = guardado.id_oferta_empresa
                trabajos.append({
                    'guardado_id': guardado.id,
                    'tipo': 'empresa',
                    'id': oferta.id,
                    'titulo': oferta.titulo_puesto,
                    'descripcion': oferta.descripcion,
                    'pago': oferta.pago,
                    'moneda': oferta.moneda,
                    'modalidad_pago': oferta.get_modalidad_pago_display(),
                    'experiencia_requerida': oferta.experiencia_requerida,
                    'vacantes': oferta.vacantes,
                    'fecha_guardado': guardado.created_at,
                    'fecha_publicacion': oferta.created_at,
                    'estado': oferta.estado,
                    'empleador': {
                        'id': oferta.id_empleador.id_usuario,
                        'nombre': oferta.id_empleador.nombre_completo,
                    },
                    'ubicacion': {
                        'departamento': oferta.id_departamento.nombre if oferta.id_departamento else None,
                        'provincia': oferta.id_provincia.nombre if oferta.id_provincia else None,
                        'distrito': oferta.id_distrito.nombre if oferta.id_distrito else None,
                    },
                    'categoria': {
                        'nombre': oferta.id_categoria.nombre if oferta.id_categoria else None,
                    },
                })
        
        context = {
            'trabajos': trabajos,
            'total_guardados': len(trabajos),
            'usuario': usuario,
        }
        
        return render(request, 'jobs/guardados/lista.html', context)
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')


@login_required
@require_POST
def guardar_trabajo(request, tipo, oferta_id):
    """
    Guardar/Marcar trabajo como favorito
    """
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        # Validar tipo
        if tipo not in ['usuario', 'empresa']:
            return JsonResponse({
                'success': False,
                'message': 'Tipo de oferta inválido'
            }, status=400)
        
        # Obtener oferta
        if tipo == 'usuario':
            oferta = get_object_or_404(OfertaUsuario, id=oferta_id, estado='activa')
            
            # Verificar si ya está guardado
            if GuardarTrabajo.objects.filter(
                id_usuario=usuario,
                id_oferta_usuario=oferta
            ).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Ya has guardado esta oferta'
                })
            
            # Guardar
            with transaction.atomic():
                GuardarTrabajo.objects.create(
                    id_usuario=usuario,
                    id_oferta_usuario=oferta
                )
            
        else:  # empresa
            oferta = get_object_or_404(OfertaEmpresa, id=oferta_id, estado='activa')
            
            # Verificar si ya está guardado
            if GuardarTrabajo.objects.filter(
                id_usuario=usuario,
                id_oferta_empresa=oferta
            ).exists():
                return JsonResponse({
                    'success': False,
                    'message': 'Ya has guardado esta oferta'
                })
            
            # Guardar
            with transaction.atomic():
                GuardarTrabajo.objects.create(
                    id_usuario=usuario,
                    id_oferta_empresa=oferta
                )
        
        return JsonResponse({
            'success': True,
            'message': '✅ Trabajo guardado exitosamente'
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
@require_POST
def quitar_guardado(request, guardado_id):
    """
    Quitar trabajo de guardados
    """
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        guardado = get_object_or_404(
            GuardarTrabajo,
            id=guardado_id,
            id_usuario=usuario
        )
        
        guardado.delete()
        
        return JsonResponse({
            'success': True,
            'message': '✅ Trabajo eliminado de guardados'
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
def trabajos_guardados_ajax(request):
    """
    Cargar trabajos guardados con AJAX (para dashboard dinámico)
    """
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        guardados = GuardarTrabajo.objects.filter(
            id_usuario=usuario
        ).select_related(
            'id_oferta_usuario',
            'id_oferta_empresa'
        ).order_by('-created_at')[:10]  # Solo los últimos 10
        
        trabajos_data = []
        for guardado in guardados:
            if guardado.id_oferta_usuario:
                oferta = guardado.id_oferta_usuario
                trabajos_data.append({
                    'guardado_id': guardado.id,
                    'tipo': 'usuario',
                    'id': oferta.id,
                    'titulo': oferta.titulo,
                    'pago': str(oferta.pago) if oferta.pago else None,
                    'estado': oferta.estado,
                    'fecha_guardado': guardado.created_at.strftime('%d/%m/%Y %H:%M'),
                })
            elif guardado.id_oferta_empresa:
                oferta = guardado.id_oferta_empresa
                trabajos_data.append({
                    'guardado_id': guardado.id,
                    'tipo': 'empresa',
                    'id': oferta.id,
                    'titulo': oferta.titulo_puesto,
                    'pago': str(oferta.pago) if oferta.pago else None,
                    'estado': oferta.estado,
                    'fecha_guardado': guardado.created_at.strftime('%d/%m/%Y %H:%M'),
                })
        
        return JsonResponse({
            'success': True,
            'trabajos': trabajos_data,
            'total': len(trabajos_data)
        })
        
    except Usuario.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Usuario no encontrado'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)