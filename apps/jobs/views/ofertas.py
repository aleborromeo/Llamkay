"""
Vistas de Gestión de Ofertas 
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction

from apps.jobs.models import OfertaUsuario, OfertaEmpresa
from apps.jobs.forms import OfertaUsuarioForm, OfertaEmpresaForm
from apps.jobs.utils import obtener_estadisticas_empleador
from apps.users.models import Usuario, Provincia, Distrito


@login_required
def registro_individual(request):
    """
    Registrar oferta individual (empleador)
    """
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        # Validar que pueda publicar ofertas
        if usuario.tipo_usuario not in ['empleador', 'ambos', 'empresa']:
            messages.error(request, "No tienes permisos para publicar ofertas.")
            return redirect('llamkay:dashboard')
        
        if request.method == 'POST':
            form = OfertaUsuarioForm(request.POST, request.FILES)
            
            if form.is_valid():
                with transaction.atomic():
                    oferta = form.save(commit=False)
                    oferta.id_empleador = usuario
                    oferta.estado = 'activa'
                    oferta.save()
                
                messages.success(request, "✅ Oferta publicada exitosamente.")
                return redirect('jobs:mis_trabajos')
            else:
                messages.error(request, "Por favor corrige los errores en el formulario.")
        else:
            form = OfertaUsuarioForm()
        
        context = {
            'form': form,
            'usuario': usuario,
        }
        return render(request, 'jobs/registro/individual.html', context)
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')


@login_required
def registro_empresa(request):
    """
    Registrar oferta de empresa
    """
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        # Validar que sea empresa
        if usuario.tipo_usuario not in ['empresa', 'empleador', 'ambos']:
            messages.error(request, "Solo empresas pueden publicar este tipo de ofertas.")
            return redirect('llamkay:dashboard')
        
        if request.method == 'POST':
            form = OfertaEmpresaForm(request.POST, request.FILES)
            
            if form.is_valid():
                with transaction.atomic():
                    oferta = form.save(commit=False)
                    oferta.id_empleador = usuario
                    oferta.estado = 'activa'
                    oferta.save()
                
                messages.success(request, "✅ Oferta publicada exitosamente.")
                return redirect('jobs:mis_trabajos')
            else:
                messages.error(request, "Por favor corrige los errores en el formulario.")
        else:
            form = OfertaEmpresaForm()
        
        context = {
            'form': form,
            'usuario': usuario,
        }
        return render(request, 'jobs/registro/empresa.html', context)
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')


@login_required
def mis_trabajos(request):
    """
    Ver trabajos publicados por el empleador
    """
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        # Obtener ofertas
        ofertas_usuario = OfertaUsuario.objects.filter(
            id_empleador=usuario
        ).select_related(
            'id_categoria',
            'id_departamento',
            'id_provincia',
            'id_distrito'
        ).order_by('-created_at')
        
        ofertas_empresa = OfertaEmpresa.objects.filter(
            id_empleador=usuario
        ).select_related(
            'id_categoria',
            'id_departamento',
            'id_provincia',
            'id_distrito'
        ).order_by('-created_at')
        
        # Obtener estadísticas
        estadisticas = obtener_estadisticas_empleador(usuario)
        
        context = {
            'ofertas_usuario': ofertas_usuario,
            'ofertas_empresa': ofertas_empresa,
            'estadisticas': estadisticas,
            'usuario': usuario,
        }
        
        return render(request, 'jobs/ofertas/mis_trabajos.html', context)
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')


@login_required
def mis_trabajos_ajax(request):
    """
    Cargar trabajos con AJAX (para dashboard dinámico)
    """
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        ofertas_usuario = OfertaUsuario.objects.filter(
            id_empleador=usuario
        ).values(
            'id', 'titulo', 'estado', 'created_at', 'vistas'
        ).order_by('-created_at')
        
        ofertas_empresa = OfertaEmpresa.objects.filter(
            id_empleador=usuario
        ).values(
            'id', 'titulo_puesto', 'estado', 'created_at', 'vistas'
        ).order_by('-created_at')
        
        # Formatear fechas
        ofertas_usuario_list = []
        for oferta in ofertas_usuario:
            oferta['created_at'] = oferta['created_at'].strftime('%d/%m/%Y %H:%M')
            ofertas_usuario_list.append(oferta)
        
        ofertas_empresa_list = []
        for oferta in ofertas_empresa:
            oferta['titulo'] = oferta.pop('titulo_puesto')
            oferta['created_at'] = oferta['created_at'].strftime('%d/%m/%Y %H:%M')
            ofertas_empresa_list.append(oferta)
        
        return JsonResponse({
            'success': True,
            'ofertas_usuario': ofertas_usuario_list,
            'ofertas_empresa': ofertas_empresa_list
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


@login_required
def editar_trabajo(request, oferta_id):
    """
    Editar una oferta de trabajo
    """
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        # Intentar obtener como OfertaUsuario
        oferta = OfertaUsuario.objects.filter(
            id=oferta_id,
            id_empleador=usuario
        ).first()
        
        tipo = 'usuario'
        FormClass = OfertaUsuarioForm
        template = 'jobs/registro/individual.html'
        
        if not oferta:
            # Intentar como OfertaEmpresa
            oferta = OfertaEmpresa.objects.filter(
                id=oferta_id,
                id_empleador=usuario
            ).first()
            tipo = 'empresa'
            FormClass = OfertaEmpresaForm
            template = 'jobs/registro/empresa.html'
        
        if not oferta:
            messages.error(request, "Oferta no encontrada.")
            return redirect('jobs:mis_trabajos')
        
        if request.method == 'POST':
            form = FormClass(request.POST, request.FILES, instance=oferta)
            
            if form.is_valid():
                with transaction.atomic():
                    form.save()
                
                messages.success(request, "✅ Oferta actualizada correctamente.")
                return redirect('jobs:mis_trabajos')
            else:
                messages.error(request, "Por favor corrige los errores en el formulario.")
        else:
            form = FormClass(instance=oferta)
        
        context = {
            'form': form,
            'oferta': oferta,
            'tipo': tipo,
            'modo_edicion': True,
            'usuario': usuario,
        }
        
        return render(request, template, context)
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')


@login_required
@require_POST
def eliminar_trabajo(request, oferta_id):
    """
    Eliminar (cerrar) una oferta
    """
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        # Intentar como OfertaUsuario
        oferta = OfertaUsuario.objects.filter(
            id=oferta_id,
            id_empleador=usuario
        ).first()
        
        if not oferta:
            # Intentar como OfertaEmpresa
            oferta = OfertaEmpresa.objects.filter(
                id=oferta_id,
                id_empleador=usuario
            ).first()
        
        if not oferta:
            return JsonResponse({
                'success': False,
                'message': 'Oferta no encontrada'
            }, status=404)
        
        # Cerrar oferta (soft delete)
        oferta.estado = 'cerrada'
        oferta.save(update_fields=['estado', 'updated_at'])
        
        return JsonResponse({
            'success': True,
            'message': 'Oferta cerrada correctamente'
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
def cambiar_estado_oferta(request, oferta_id):
    """
    Cambiar estado de una oferta (activa/pausada)
    """
    try:
        usuario = Usuario.objects.get(user=request.user)
        nuevo_estado = request.POST.get('estado')
        
        if nuevo_estado not in ['activa', 'pausada', 'cerrada']:
            return JsonResponse({
                'success': False,
                'message': 'Estado inválido'
            }, status=400)
        
        # Buscar oferta
        oferta = OfertaUsuario.objects.filter(
            id=oferta_id,
            id_empleador=usuario
        ).first()
        
        if not oferta:
            oferta = OfertaEmpresa.objects.filter(
                id=oferta_id,
                id_empleador=usuario
            ).first()
        
        if not oferta:
            return JsonResponse({
                'success': False,
                'message': 'Oferta no encontrada'
            }, status=404)
        
        # Cambiar estado
        oferta.estado = nuevo_estado
        oferta.save(update_fields=['estado', 'updated_at'])
        
        return JsonResponse({
            'success': True,
            'message': f'Oferta {nuevo_estado} correctamente',
            'nuevo_estado': nuevo_estado
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


# AJAX para ubicación
def cargar_provincias(request):
    """Cargar provincias por departamento"""
    id_departamento = request.GET.get('id_departamento')
    
    if not id_departamento:
        return JsonResponse([], safe=False)
    
    try:
        provincias = Provincia.objects.filter(
            id_departamento=id_departamento
        ).values('id_provincia', 'nombre').order_by('nombre')
        
        return JsonResponse(list(provincias), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def cargar_distritos(request):
    """Cargar distritos por provincia"""
    id_provincia = request.GET.get('id_provincia')
    
    if not id_provincia:
        return JsonResponse([], safe=False)
    
    try:
        distritos = Distrito.objects.filter(
            id_provincia=id_provincia
        ).values('id_distrito', 'nombre').order_by('nombre')
        
        return JsonResponse(list(distritos), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


def cargar_comunidades(request):
    """Cargar comunidades por distrito"""
    from apps.users.models import Comunidad
    
    id_distrito = request.GET.get('id_distrito')
    
    if not id_distrito:
        return JsonResponse([], safe=False)
    
    try:
        comunidades = Comunidad.objects.filter(
            id_distrito=id_distrito
        ).values('id_comunidad', 'nombre').order_by('nombre')
        
        return JsonResponse(list(comunidades), safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)