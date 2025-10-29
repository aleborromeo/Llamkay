from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from apps.users.models import Usuario, Provincia, Distrito
from apps.empleadores.services import OfertaService
from apps.empleadores.forms import OfertaUsuarioForm, OfertaEmpresaForm


oferta_service = OfertaService()


@login_required
def registro_individual(request):
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        if usuario.tipo_usuario not in ['empleador', 'ambos', 'empresa']:
            messages.error(request, "No tienes permisos para publicar ofertas.")
            return redirect('llamkay:dashboard')
        
        if request.method == 'POST':
            form = OfertaUsuarioForm(request.POST, request.FILES)
            
            if form.is_valid():
                form_data = form.cleaned_data
                resultado = oferta_service.crear_oferta_individual(
                    usuario.id_usuario,
                    form_data
                )
                
                if resultado['success']:
                    messages.success(request, resultado['message'])
                    return redirect('empleadores:mis_trabajos')
                else:
                    messages.error(request, resultado['message'])
            else:
                messages.error(request, "Por favor corrige los errores en el formulario.")
        else:
            form = OfertaUsuarioForm()
        
        context = {
            'form': form,
            'usuario': usuario,
        }
        return render(request, 'empleadores/ofertas/individual.html', context)
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')


@login_required
def registro_empresa(request):
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        if usuario.tipo_usuario not in ['empresa', 'empleador', 'ambos']:
            messages.error(request, "Solo empresas pueden publicar este tipo de ofertas.")
            return redirect('llamkay:dashboard')
        
        if request.method == 'POST':
            form = OfertaEmpresaForm(request.POST, request.FILES)
            
            if form.is_valid():
                form_data = form.cleaned_data
                resultado = oferta_service.crear_oferta_empresa(
                    usuario.id_usuario,
                    form_data
                )
                
                if resultado['success']:
                    messages.success(request, resultado['message'])
                    return redirect('empleadores:mis_trabajos')
                else:
                    messages.error(request, resultado['message'])
            else:
                messages.error(request, "Por favor corrige los errores en el formulario.")
        else:
            form = OfertaEmpresaForm()
        
        context = {
            'form': form,
            'usuario': usuario,
        }
        return render(request, 'empleadores/ofertas/empresa.html', context)
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')


@login_required
def mis_trabajos(request):
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        ofertas_data = oferta_service.get_mis_ofertas(usuario.id_usuario)
        estadisticas = oferta_service.get_estadisticas(usuario.id_usuario)
        
        context = {
            'ofertas_usuario': ofertas_data['ofertas_usuario'],
            'ofertas_empresa': ofertas_data['ofertas_empresa'],
            'estadisticas': estadisticas,
            'usuario': usuario,
        }
        
        return render(request, 'empleadores/ofertas/mis_trabajos.html', context)
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')


@login_required
def mis_trabajos_ajax(request):
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        ofertas = oferta_service.get_ofertas_activas_recientes(usuario.id_usuario, limit=10)
        
        return JsonResponse({
            'success': True,
            'ofertas': ofertas
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
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        resultado = oferta_service.get_oferta_para_editar(oferta_id, usuario.id_usuario)
        
        if not resultado:
            messages.error(request, "Oferta no encontrada.")
            return redirect('empleadores:mis_trabajos')
        
        oferta, tipo = resultado
        
        if tipo == 'usuario':
            FormClass = OfertaUsuarioForm
            template = 'empleadores/ofertas/individual.html'
        else:
            FormClass = OfertaEmpresaForm
            template = 'empleadores/ofertas/empresa.html'
        
        if request.method == 'POST':
            form = FormClass(request.POST, request.FILES, instance=oferta)
            
            if form.is_valid():
                form_data = form.cleaned_data
                resultado_update = oferta_service.actualizar_oferta(
                    oferta_id,
                    usuario.id_usuario,
                    tipo,
                    form_data
                )
                
                if resultado_update['success']:
                    messages.success(request, resultado_update['message'])
                    return redirect('empleadores:mis_trabajos')
                else:
                    messages.error(request, resultado_update['message'])
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
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        resultado = oferta_service.get_oferta_para_editar(oferta_id, usuario.id_usuario)
        
        if not resultado:
            return JsonResponse({
                'success': False,
                'message': 'Oferta no encontrada'
            }, status=404)
        
        _, tipo = resultado
        
        resultado_cambio = oferta_service.cambiar_estado(
            oferta_id,
            usuario.id_usuario,
            'cerrada',
            tipo
        )
        
        return JsonResponse(resultado_cambio)
        
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
    try:
        usuario = Usuario.objects.get(user=request.user)
        nuevo_estado = request.POST.get('estado')
        
        if nuevo_estado not in ['activa', 'pausada', 'cerrada']:
            return JsonResponse({
                'success': False,
                'message': 'Estado inválido'
            }, status=400)
        
        resultado = oferta_service.get_oferta_para_editar(oferta_id, usuario.id_usuario)
        
        if not resultado:
            return JsonResponse({
                'success': False,
                'message': 'Oferta no encontrada'
            }, status=404)
        
        _, tipo = resultado
        
        resultado_cambio = oferta_service.cambiar_estado(
            oferta_id,
            usuario.id_usuario,
            nuevo_estado,
            tipo
        )
        
        return JsonResponse(resultado_cambio)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        }, status=500)


def cargar_provincias(request):
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