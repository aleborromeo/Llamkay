from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from functools import wraps
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie

from apps.users.models import Usuario
from apps.empleadores.services import PostulanteService
from apps.empleadores.repositories import OfertaEmpleadorRepository

postulante_service = PostulanteService()
oferta_repo = OfertaEmpleadorRepository()


@login_required
def ver_postulantes(request, oferta_id, tipo):
    try:
        usuario = Usuario.objects.get(user=request.user)

        # validar tipo
        if tipo not in ['usuario', 'empresa']:
            messages.error(request, "Tipo de oferta inválido.")
            return redirect('empleadores:mis_trabajos')

        # obtener la oferta según el tipo, validando que pertenezca al empleador
        if tipo == 'usuario':
            oferta = oferta_repo.get_oferta_usuario_by_id_empleador(
                oferta_id, usuario.id_usuario
            )
        else:
            oferta = oferta_repo.get_oferta_empresa_by_id_empleador(
                oferta_id, usuario.id_usuario
            )

        if not oferta:
            messages.error(request, "Oferta no encontrada o no te pertenece.")
            return redirect('empleadores:mis_trabajos')

        estado_filtro = request.GET.get('estado')

        resultado = postulante_service.get_postulantes_oferta(
            oferta_id,
            tipo,
            usuario.id_usuario,
            estado=estado_filtro
        )

        postulaciones = resultado['postulaciones']
        estadisticas = resultado['estadisticas']

        context = {
            'oferta': oferta,
            'tipo': tipo,
            'estado_filtro': estado_filtro,
            'usuario': usuario,
            'postulaciones': postulaciones,
            'estadisticas': estadisticas,
            'total_postulaciones': estadisticas['total'],
            'pendientes': estadisticas['pendientes'],
            'aceptadas': estadisticas['aceptadas'],
            'rechazadas': estadisticas['rechazadas'],
        }

        return render(request, 'empleadores/postulantes/ver.html', context)

    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')

def ajax_login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({
                'success': False,
                'message': 'No autenticado'
            }, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view



@require_POST
@ajax_login_required
def aceptar_postulante(request, postulacion_id):
    """Vista para aceptar un postulante - SOLO maneja AJAX"""
    
    print("="*80)
    print("🔵 VISTA ACEPTAR_POSTULANTE LLAMADA")
    print(f"  - Método: {request.method}")
    print(f"  - AJAX: {request.headers.get('X-Requested-With')}")
    print(f"  - Autenticado: {request.user.is_authenticated}")
    print(f"  - Usuario: {request.user}")
    print(f"  - Postulación ID: {postulacion_id}")
    print("="*80)
    
    # Verificar autenticación
    if not request.user.is_authenticated:
        print("❌ Usuario NO autenticado")
        return JsonResponse({
            'success': False,
            'message': 'Debes iniciar sesión'
        }, status=401)
    
    try:
        usuario = Usuario.objects.get(user=request.user)
        print(f"✅ Usuario encontrado: {usuario.nombre_completo} (ID: {usuario.id_usuario})")
        
        resultado = postulante_service.aceptar_postulante(
            postulacion_id,
            usuario.id_usuario
        )
        
        print(f"📦 Resultado del servicio: {resultado}")
        print("="*80)
        
        # SIEMPRE devolver JSON, nunca redirect
        return JsonResponse(resultado)

    except Usuario.DoesNotExist:
        print("❌ Usuario no existe en BD")
        return JsonResponse({
            'success': False,
            'message': 'Usuario no encontrado'
        }, status=404)
        
    except Exception as e:
        print(f"💥 ERROR CRÍTICO: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error del servidor: {str(e)}'
        }, status=500)


@require_POST
@ajax_login_required
def rechazar_postulante(request, postulacion_id):
    """Vista para rechazar un postulante - SOLO maneja AJAX"""
    
    print("="*80)
    print("🔴 VISTA RECHAZAR_POSTULANTE LLAMADA")
    print(f"  - Método: {request.method}")
    print(f"  - AJAX: {request.headers.get('X-Requested-With')}")
    print(f"  - Autenticado: {request.user.is_authenticated}")
    print(f"  - Usuario: {request.user}")
    print(f"  - Postulación ID: {postulacion_id}")
    print("="*80)
    
    # Verificar autenticación
    if not request.user.is_authenticated:
        print("❌ Usuario NO autenticado")
        return JsonResponse({
            'success': False,
            'message': 'Debes iniciar sesión'
        }, status=401)
    
    try:
        usuario = Usuario.objects.get(user=request.user)
        print(f"✅ Usuario encontrado: {usuario.nombre_completo} (ID: {usuario.id_usuario})")
        
        resultado = postulante_service.rechazar_postulante(
            postulacion_id,
            usuario.id_usuario
        )
        
        print(f"📦 Resultado del servicio: {resultado}")
        print("="*80)
        
        # SIEMPRE devolver JSON, nunca redirect
        return JsonResponse(resultado)

    except Usuario.DoesNotExist:
        print("❌ Usuario no existe en BD")
        return JsonResponse({
            'success': False,
            'message': 'Usuario no encontrado'
        }, status=404)
        
    except Exception as e:
        print(f"💥 ERROR CRÍTICO: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error del servidor: {str(e)}'
        }, status=500)


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