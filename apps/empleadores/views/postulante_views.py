from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_http_methods
from apps.empleadores.decorators import ajax_login_required


from apps.users.models import Usuario
from apps.empleadores.services import PostulanteService
from apps.empleadores.repositories import OfertaEmpleadorRepository  # 👈 nuevo import

postulante_service = PostulanteService()
oferta_repo = OfertaEmpleadorRepository()  # 👈 repositorio de ofertas


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

        postulaciones = resultado['postulaciones']          # lista de dicts
        estadisticas = resultado['estadisticas']            # dict con totales

        context = {
            'oferta': oferta,
            'tipo': tipo,
            'estado_filtro': estado_filtro,
            'usuario': usuario,

            # lista para recorrer en el template
            'postulaciones': postulaciones,

            # estadísticas desde el servicio
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





@ajax_login_required  # <-- Usa este en lugar de @login_required
@require_POST



@require_POST
def aceptar_postulante(request, postulacion_id):
    print("=" * 50)
    print("🔍 INICIO DE LA VISTA")
    print(f"Usuario autenticado: {request.user.is_authenticated}")
    print(f"Usuario: {request.user}")
    print(f"Método: {request.method}")
    print(f"Headers: {dict(request.headers)}")
    print("=" * 50)
    
    # Verificar autenticación manualmente
    if not request.user.is_authenticated:
        print("❌ Usuario no autenticado")
        return JsonResponse({
            'success': False,
            'message': 'Debes iniciar sesión'
        }, status=401)
    
    # Verificar que sea AJAX
    if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        print("❌ No es petición AJAX")
        return JsonResponse({
            'success': False,
            'message': 'Petición inválida'
        }, status=400)
    
    try:
        usuario = Usuario.objects.get(user=request.user)
        print(f"✅ Usuario encontrado: {usuario}")

        resultado = postulante_service.aceptar_postulante(
            postulacion_id,
            usuario.id_usuario
        )

        print(f"✅ Resultado del servicio: {resultado}")
        print("=" * 50)
        
        return JsonResponse(resultado)

    except Usuario.DoesNotExist:
        print("❌ Usuario no existe en la BD")
        return JsonResponse({
            'success': False,
            'message': 'Usuario no encontrado'
        }, status=404)
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'success': False,
            'message': f'Error del servidor: {str(e)}'
        }, status=500)
        
@login_required
@require_POST
def rechazar_postulante(request, postulacion_id):
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        resultado = postulante_service.rechazar_postulante(
            postulacion_id,
            usuario.id_usuario
        )
        
        is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

        if is_ajax:
            return JsonResponse(resultado)

        return redirect('empleadores:mis_trabajos')
        
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