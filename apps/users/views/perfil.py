from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.db import transaction

from apps.users.models import (
    Usuario, Profile, Certificacion,
    TrabajosRealizados, Departamento, Provincia, Distrito
)

from apps.jobs.models import Calificacion

@login_required
def perfil(request):
    """Vista principal del perfil del usuario"""
    try:
        usuario_db = Usuario.objects.get(user=request.user)
        profile, _ = Profile.objects.get_or_create(
            user=request.user, 
            id_usuario=usuario_db
        )

        certificaciones = Certificacion.objects.filter(id_usuario=usuario_db)
        trabajos_realizados = TrabajosRealizados.objects.filter(
            id_usuario=usuario_db
        ).order_by('-fecha_inicio')
        calificaciones = Calificacion.objects.filter(
            id_receptor=usuario_db
        ).select_related('id_autor')

        context = {
            'usuario': usuario_db,
            'profile': profile,
            'certificaciones': certificaciones,
            'trabajos_realizados': trabajos_realizados,
            'calificaciones': calificaciones,
        }

        return render(request, 'users/profile/profile.html', context)

    except Usuario.DoesNotExist:
        messages.error(request, "No se encontró tu perfil.")
        return redirect('users:login')


@login_required
@require_POST
@transaction.atomic
def actualizar_perfil(request):
    """Actualizar información del perfil"""
    try:
        usuario_db = Usuario.objects.get(user=request.user)
        profile, _ = Profile.objects.get_or_create(
            user=request.user, 
            id_usuario=usuario_db
        )

        # Actualizar campos básicos
        telefono = request.POST.get('telefono', '').strip()
        if telefono:
            usuario_db.telefono = telefono
        usuario_db.save()

        # Actualizar bio
        descripcion = request.POST.get('descripcion', '').strip()
        if descripcion:
            profile.bio = descripcion

        # Actualizar foto
        if 'foto' in request.FILES:
            profile.foto_url = request.FILES['foto']

        # Actualizar ubicación
        for campo, modelo, attr in [
            ('id_departamento', Departamento, 'id_departamento'),
            ('id_provincia', Provincia, 'id_provincia'),
            ('id_distrito', Distrito, 'id_distrito')
        ]:
            valor = request.POST.get(campo)
            if valor:
                obj = modelo.objects.filter(**{attr: valor}).first()
                if obj:
                    setattr(profile, attr, obj)

        profile.save()

        return JsonResponse({
            'status': 'ok', 
            'message': 'Perfil actualizado correctamente.'
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error', 
            'message': str(e)
        }, status=500)


@login_required
def exportar_portafolio_pdf(request):
    """Exportar portafolio como PDF"""
    try:
        from xhtml2pdf import pisa
        from django.template.loader import get_template
        from io import BytesIO

        usuario_db = Usuario.objects.get(user=request.user)
        profile = Profile.objects.get(user=request.user)
        
        certificaciones = Certificacion.objects.filter(id_usuario=usuario_db)
        trabajos = TrabajosRealizados.objects.filter(id_usuario=usuario_db)

        template = get_template('users/portafolio_pdf.html')
        context = {
            'usuario': usuario_db,
            'profile': profile,
            'certificaciones': certificaciones,
            'trabajos': trabajos,
        }
        html = template.render(context)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="portafolio.pdf"'
        
        pisa_status = pisa.CreatePDF(
            BytesIO(html.encode("utf-8")), 
            dest=response
        )
        
        if pisa_status.err:
            return HttpResponse('Error al generar PDF', status=500)
        
        return response

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)