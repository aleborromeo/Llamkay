"""
Vistas de Perfil - REFACTORIZADAS Y CORREGIDAS
Responsabilidad: Solo manejar request/response (SRP)
La lógica está en los servicios
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.db import transaction

from apps.users.services import PerfilService
from apps.users.repositories import UsuarioRepository
from apps.users.models import Usuario, Departamento, Provincia, Distrito


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
        
        return render(request, 'users/profile/profile.html', context)
        
    except ValueError as e:
        messages.error(request, str(e))
        return redirect('users:login')
    except Exception as e:
        messages.error(request, f"Error al cargar perfil: {str(e)}")
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
@require_POST
@transaction.atomic
def actualizar_perfil(request):
    """
    Actualizar información del perfil
    """
    try:
        usuario_repo = UsuarioRepository()
        usuario = usuario_repo.obtener_por_user(request.user)
        
        if not usuario:
            return JsonResponse({
                'status': 'error',
                'message': 'Usuario no encontrado.'
            }, status=404)
        
        # Obtener el perfil
        from apps.users.models import Profile
        profile = Profile.objects.filter(user=request.user).first()
        
        if not profile:
            return JsonResponse({
                'status': 'error',
                'message': 'Perfil no encontrado.'
            }, status=404)
        
        # Actualizar teléfono en Usuario
        telefono = request.POST.get('telefono', '').strip()
        if telefono:
            if not telefono.isdigit() or len(telefono) != 9:
                return JsonResponse({
                    'status': 'error',
                    'message': 'El teléfono debe tener 9 dígitos numéricos.'
                }, status=400)
            usuario.telefono = telefono
            usuario.save()
        
        # Actualizar descripción en Profile
        descripcion = request.POST.get('descripcion', '').strip()
        if descripcion:
            profile.bio = descripcion
        
        # Actualizar tarifa por hora
        tarifa_hora = request.POST.get('tarifa_hora', '').strip()
        if tarifa_hora:
            try:
                tarifa = float(tarifa_hora)
                if tarifa < 0:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'La tarifa debe ser un número positivo.'
                    }, status=400)
                profile.tarifa_hora = tarifa
            except ValueError:
                return JsonResponse({
                    'status': 'error',
                    'message': 'La tarifa debe ser un número válido.'
                }, status=400)
        
        # Actualizar disponibilidad (guardar en algún campo del profile)
        disponibilidad = request.POST.get('disponibilidad', '').strip()
        # Si tienes un campo disponibilidad en Profile, úsalo:
        # profile.disponibilidad = disponibilidad
        
        # Actualizar ubicación (convertir IDs a instancias)
        id_departamento = request.POST.get('id_departamento')
        if id_departamento:
            try:
                departamento = Departamento.objects.get(id_departamento=id_departamento)
                profile.id_departamento = departamento
            except Departamento.DoesNotExist:
                pass
        
        id_provincia = request.POST.get('id_provincia')
        if id_provincia:
            try:
                provincia = Provincia.objects.get(id_provincia=id_provincia)
                profile.id_provincia = provincia
            except Provincia.DoesNotExist:
                pass
        
        id_distrito = request.POST.get('id_distrito')
        if id_distrito:
            try:
                distrito = Distrito.objects.get(id_distrito=id_distrito)
                profile.id_distrito = distrito
            except Distrito.DoesNotExist:
                pass
        
        # Actualizar foto si se envió
        if 'foto' in request.FILES:
            foto = request.FILES['foto']
            
            # Validar tipo de archivo
            if not foto.content_type.startswith('image/'):
                return JsonResponse({
                    'status': 'error',
                    'message': 'El archivo debe ser una imagen.'
                }, status=400)
            
            # Validar tamaño (5MB)
            if foto.size > 5 * 1024 * 1024:
                return JsonResponse({
                    'status': 'error',
                    'message': 'La imagen no debe superar los 5MB.'
                }, status=400)
            
            profile.foto_url = foto
        
        # Guardar cambios
        profile.save()
        
        return JsonResponse({
            'status': 'ok',
            'message': 'Perfil actualizado correctamente.'
        })
            
    except Exception as e:
        print(f"Error al actualizar perfil: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return JsonResponse({
            'status': 'error',
            'message': f'Error: {str(e)}'
        }, status=500)

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