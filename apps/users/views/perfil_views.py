"""
Vistas de Perfil - REFACTORIZADAS
Responsabilidad: Solo manejar request/response (SRP)
La lógica está en los servicios
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_http_methods
from django.db import transaction
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

from apps.users.services import PerfilService
from apps.users.repositories import UsuarioRepository
from apps.users.models import Usuario


@login_required
def perfil(request):
    """
    Vista principal del perfil del usuario
    Delegada completamente al servicio
    """
    try:
        # Inyectar servicio
        perfil_service = PerfilService()
        
        # Obtener datos (toda la lógica en el servicio)
        context = perfil_service.obtener_datos_completos(request.user)
        
        logger.info(f"✅ Perfil cargado para: {request.user.username}")
        return render(request, 'users/profile/profile.html', context)
        
    except ValueError as e:
        logger.error(f"❌ ValueError en perfil: {str(e)}")
        messages.error(request, str(e))
        return redirect('users:login')
    except Exception as e:
        logger.error(f"❌ Error en perfil: {str(e)}", exc_info=True)
        messages.error(request, f"Error al cargar perfil: {str(e)}")
        
        # Contexto mínimo de emergencia
        try:
            from apps.users.models import Usuario
            usuario_obj = Usuario.objects.get(user=request.user)
            context = {
                'usuario': usuario_obj,
                'profile': None,
            }
            return render(request, 'users/profile/profile.html', context)
        except:
            return redirect('llamkay:dashboard')


def perfil_publico(request, usuario_id):
    """
    Vista del perfil público de un usuario
    """
    try:
        perfil_service = PerfilService()
        context = perfil_service.obtener_perfil_publico(usuario_id)
        
        return render(request, 'users/profile/perfil_publico.html', context)
        
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('llamkay:dashboard')
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('llamkay:dashboard')


@login_required
@require_http_methods(["GET", "POST"])
@transaction.atomic
def actualizar_perfil(request):
    """
    Actualizar información del perfil
    Soporta tanto peticiones normales como AJAX
    """
    # Si es GET, redirigir a perfil
    if request.method == 'GET':
        return redirect('users:perfil')
    
    try:
        perfil_service = PerfilService()
        
        # Preparar datos del request
        datos = {
            'telefono': request.POST.get('telefono', '').strip(),
            'descripcion': request.POST.get('descripcion', '').strip(),
            'bio': request.POST.get('bio', '').strip(),
            'ocupacion': request.POST.get('ocupacion', '').strip(),
        }
        
        # Ubicación
        if request.POST.get('id_departamento'):
            datos['id_departamento'] = request.POST.get('id_departamento')
        if request.POST.get('id_provincia'):
            datos['id_provincia'] = request.POST.get('id_provincia')
        if request.POST.get('id_distrito'):
            datos['id_distrito'] = request.POST.get('id_distrito')
        
        # Tarifa
        tarifa_hora = request.POST.get('tarifa_hora', '').strip()
        if tarifa_hora and tarifa_hora != 'None':
            try:
                datos['tarifa_hora'] = Decimal(tarifa_hora)
            except Exception as e:
                logger.warning(f"Tarifa inválida: {tarifa_hora} - {e}")
        
        # Agregar foto si existe
        if 'foto' in request.FILES:
            foto = request.FILES['foto']
            # Validar tamaño (máx 5MB)
            if foto.size > 5 * 1024 * 1024:
                raise ValueError("La foto no puede pesar más de 5MB")
            # Validar tipo
            if not foto.content_type.startswith('image/'):
                raise ValueError("El archivo debe ser una imagen")
            datos['foto'] = foto
        
        # Delegar al servicio
        exito = perfil_service.actualizar_perfil(request.user, datos)
        
        if exito:
            logger.info(f"✅ Perfil actualizado: {request.user.email}")
            
            # Si es petición AJAX, devolver JSON
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'ok',
                    'message': 'Perfil actualizado correctamente.'
                })
            
            # Si es petición normal, redirigir con mensaje
            messages.success(request, '✅ Perfil actualizado correctamente.')
            return redirect('users:perfil')
        else:
            logger.error(f"❌ Error actualizando perfil de {request.user.email}")
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'error',
                    'message': 'Error al actualizar perfil.'
                }, status=500)
            
            messages.error(request, '❌ Error al actualizar perfil.')
            return redirect('users:perfil')
            
    except ValueError as e:
        logger.warning(f"⚠️ Validación fallida: {str(e)}")
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
        
        messages.error(request, f'❌ {str(e)}')
        return redirect('users:perfil')
        
    except Exception as e:
        logger.error(f"❌ Error en actualizar_perfil: {str(e)}", exc_info=True)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'error',
                'message': f'Error: {str(e)}'
            }, status=500)
        
        messages.error(request, f'❌ Error: {str(e)}')
        return redirect('users:perfil')

@login_required
def exportar_portafolio_pdf(request):
    """
    Exportar portafolio como PDF
    """
    try:
        from xhtml2pdf import pisa
        from django.template.loader import get_template
        from io import BytesIO
        
        # Usar servicio para obtener datos
        perfil_service = PerfilService()
        context = perfil_service.exportar_portafolio(request.user)
        
        # Renderizar template
        template = get_template('users/profile/portafolio_pdf.html')
        html = template.render(context)
        
        # Generar PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="portafolio_{context["usuario"].username}.pdf"'
        
        pisa_status = pisa.CreatePDF(
            BytesIO(html.encode("utf-8")),
            dest=response
        )
        
        if pisa_status.err:
            return HttpResponse('Error al generar PDF', status=500)
        
        return response
        
    except Exception as e:
        messages.error(request, f"Error al generar PDF: {str(e)}")
        return redirect('users:perfil')