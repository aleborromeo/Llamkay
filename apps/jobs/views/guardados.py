from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from apps.jobs.models import OfertaUsuario, OfertaEmpresa, GuardarTrabajo
from apps.users.models import Usuario


@login_required
def trabajos_guardados(request):
    """Lista de trabajos guardados por el usuario"""
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        guardados = GuardarTrabajo.objects.filter(
            id_usuario=usuario
        ).select_related(
            'id_oferta_usuario',
            'id_oferta_empresa'
        ).order_by('-fecha_guardado')
        
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
                    'fecha_guardado': guardado.fecha_guardado,
                    'nota_personal': guardado.nota_personal,
                    'estado': oferta.estado,
                })
            elif guardado.id_oferta_empresa:
                oferta = guardado.id_oferta_empresa
                trabajos.append({
                    'guardado_id': guardado.id,
                    'tipo': 'empresa',
                    'id': oferta.id,
                    'titulo': oferta.titulo_puesto,
                    'descripcion': oferta.descripcion,
                    'rango_salarial': f"{oferta.pago} {oferta.moneda}" if oferta.pago else None,
                    'fecha_guardado': guardado.fecha_guardado,
                    'nota_personal': guardado.nota_personal,
                    'estado': oferta.estado,
                })
        
        context = {
            'trabajos': trabajos,
        }
        
        return render(request, 'jobs/guardados/lista.html', context)
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')


@login_required
@require_POST
def guardar_trabajo(request, tipo, oferta_id):
    """Guardar/Marcar trabajo como favorito"""
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        if tipo == 'usuario':
            oferta = get_object_or_404(OfertaUsuario, id=oferta_id)
            
            # Verificar si ya está guardado
            ya_guardado = GuardarTrabajo.objects.filter(
                id_usuario=usuario,
                id_oferta_usuario=oferta
            ).exists()
            
            if ya_guardado:
                return JsonResponse({
                    'success': False,
                    'message': 'Ya has guardado esta oferta'
                })
            
            GuardarTrabajo.objects.create(
                id_usuario=usuario,
                id_oferta_usuario=oferta
            )
            
        elif tipo == 'empresa':
            oferta = get_object_or_404(OfertaEmpresa, id=oferta_id)
            
            ya_guardado = GuardarTrabajo.objects.filter(
                id_usuario=usuario,
                id_oferta_empresa=oferta
            ).exists()
            
            if ya_guardado:
                return JsonResponse({
                    'success': False,
                    'message': 'Ya has guardado esta oferta'
                })
            
            GuardarTrabajo.objects.create(
                id_usuario=usuario,
                id_oferta_empresa=oferta
            )
        else:
            return JsonResponse({
                'success': False,
                'message': 'Tipo de oferta inválido'
            }, status=400)
        
        return JsonResponse({
            'success': True,
            'message': 'Trabajo guardado exitosamente'
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
    """Quitar trabajo de guardados"""
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
            'message': 'Trabajo eliminado de guardados'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


@login_required
@require_POST
def agregar_nota_guardado(request, guardado_id):
    """Agregar nota personal a trabajo guardado"""
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        guardado = get_object_or_404(
            GuardarTrabajo,
            id=guardado_id,
            id_usuario=usuario
        )
        
        nota = request.POST.get('nota', '').strip()
        guardado.nota_personal = nota
        guardado.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Nota guardada correctamente'
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)