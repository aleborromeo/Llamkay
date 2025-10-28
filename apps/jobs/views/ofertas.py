from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Count

from apps.jobs.models import OfertaUsuario, OfertaEmpresa, GuardarTrabajo, Postulacion
from apps.users.models import Usuario, Departamento, Provincia, Distrito


def all_trabajos(request):
    """Vista principal que muestra todos los trabajos disponibles"""

    # Parámetros de búsqueda
    buscar = request.GET.get('buscar', '').strip()
    departamento_id = request.GET.get('departamento_id')
    provincia_id = request.GET.get('provincia_id')
    distrito_id = request.GET.get('distrito_id')
    tipo_usuario = request.GET.get('tipo_usuario', '')

    trabajos = []

    # ================== OFERTAS DE USUARIOS ==================
    if tipo_usuario in ('', 'empleador'):
        queryset_usuario = OfertaUsuario.objects.select_related(
            'id_empleador', 'id_categoria', 'id_departamento', 'id_provincia', 'id_distrito'
        ).filter(estado='activa')

        if buscar:
            queryset_usuario = queryset_usuario.filter(
                Q(titulo__icontains=buscar) |
                Q(descripcion__icontains=buscar) |
                Q(id_categoria__nombre__icontains=buscar)
            )

        if departamento_id:
            queryset_usuario = queryset_usuario.filter(id_departamento=departamento_id)
        if provincia_id:
            queryset_usuario = queryset_usuario.filter(id_provincia=provincia_id)
        if distrito_id:
            queryset_usuario = queryset_usuario.filter(id_distrito=distrito_id)

        for oferta in queryset_usuario:
            trabajos.append({
                'tipo': 'usuario',
                'id': oferta.id,
                'titulo': oferta.titulo,
                'descripcion': oferta.descripcion,
                'pago': f"{oferta.pago} {oferta.moneda}" if oferta.pago else None,
                'modalidad_pago': oferta.get_modalidad_pago_display(),
                'fecha_publicacion': oferta.created_at,  # ✅ Cambiado
                'urgente': oferta.urgente,
                'empleador': oferta.id_empleador,
                'categoria': oferta.id_categoria.nombre if oferta.id_categoria else '',
                'ubicacion': {
                    'departamento': oferta.id_departamento.nombre if oferta.id_departamento else '',
                    'provincia': oferta.id_provincia.nombre if oferta.id_provincia else '',
                    'distrito': oferta.id_distrito.nombre if oferta.id_distrito else '',
                },
            })

    # ================== OFERTAS DE EMPRESAS ==================
    if tipo_usuario in ('', 'empresa'):
        queryset_empresa = OfertaEmpresa.objects.select_related(
            'id_empleador', 'id_categoria', 'id_departamento', 'id_provincia', 'id_distrito'
        ).filter(estado='activa')

        if buscar:
            queryset_empresa = queryset_empresa.filter(
                Q(titulo_puesto__icontains=buscar) |
                Q(descripcion__icontains=buscar) |
                Q(id_categoria__nombre__icontains=buscar)
            )

        if departamento_id:
            queryset_empresa = queryset_empresa.filter(id_departamento=departamento_id)
        if provincia_id:
            queryset_empresa = queryset_empresa.filter(id_provincia=provincia_id)
        if distrito_id:
            queryset_empresa = queryset_empresa.filter(id_distrito=distrito_id)

        for oferta in queryset_empresa:
            trabajos.append({
                'tipo': 'empresa',
                'id': oferta.id,
                'titulo': oferta.titulo_puesto,
                'descripcion': oferta.descripcion,
                'pago': f"{oferta.pago} {oferta.moneda}" if oferta.pago else None,
                'modalidad_pago': oferta.get_modalidad_pago_display(),
                'fecha_publicacion': oferta.created_at,  # ✅ Cambiado
                'empleador': oferta.id_empleador,
                'categoria': oferta.id_categoria.nombre if oferta.id_categoria else '',
                'ubicacion': {
                    'departamento': oferta.id_departamento.nombre if oferta.id_departamento else '',
                    'provincia': oferta.id_provincia.nombre if oferta.id_provincia else '',
                    'distrito': oferta.id_distrito.nombre if oferta.id_distrito else '',
                },
                'vacantes': oferta.vacantes,
            })

    # ================== ORDENAR RESULTADOS ==================
    trabajos.sort(key=lambda x: x['fecha_publicacion'], reverse=True)

    # ================== TRABAJOS GUARDADOS ==================
    trabajos_guardados_ids = set()
    if request.user.is_authenticated:
        try:
            usuario = Usuario.objects.get(user=request.user)
            guardados = GuardarTrabajo.objects.filter(id_usuario=usuario)

            for g in guardados:
                if g.id_oferta_usuario:
                    trabajos_guardados_ids.add(f"usuario_{g.id_oferta_usuario.id}")
                elif g.id_oferta_empresa:
                    trabajos_guardados_ids.add(f"empresa_{g.id_oferta_empresa.id}")
        except Usuario.DoesNotExist:
            pass

    # ================== CONTEXTO ==================
    departamentos = Departamento.objects.all().order_by('nombre')

    context = {
        'trabajos': trabajos,
        'departamentos': departamentos,
        'trabajos_guardados_ids': trabajos_guardados_ids,
        'filtros': {
            'buscar': buscar,
            'departamento_id': departamento_id,
            'provincia_id': provincia_id,
            'distrito_id': distrito_id,
            'tipo_usuario': tipo_usuario,
        },
    }

    return render(request, 'jobs/all_trabajos.html', context)


def filtrar_trabajos(request):
    """Filtrar trabajos con AJAX"""
    # Redirigir a all_trabajos con los parámetros
    return redirect('jobs:all_trabajos')


@login_required
def registro_individual(request):
    """Registrar oferta individual (empleador)"""
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        # ✅ Validación opcional del tipo de usuario
        # if hasattr(usuario, 'tipo_usuario') and usuario.tipo_usuario not in ['empleador', 'ambos']:
        #     messages.error(request, "No tienes permiso para publicar ofertas.")
        #     return redirect('llamkay:dashboard')
        
        if request.method == 'POST':
            from apps.jobs.forms import OfertaUsuarioForm
            form = OfertaUsuarioForm(request.POST, request.FILES)
            
            if form.is_valid():
                oferta = form.save(commit=False)
                oferta.id_empleador = usuario
                oferta.save()
                
                messages.success(request, "Oferta publicada exitosamente.")
                return redirect('jobs:mis_trabajos')
        else:
            from apps.jobs.forms import OfertaUsuarioForm
            form = OfertaUsuarioForm()
        
        return render(request, 'jobs/registro/individual.html', {'form': form})
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')


@login_required
def registro_empresa(request):
    """Registrar oferta de empresa"""
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        # ✅ Validación opcional
        # if hasattr(usuario, 'tipo_usuario') and usuario.tipo_usuario != 'empresa':
        #     messages.error(request, "Solo empresas pueden publicar este tipo de ofertas.")
        #     return redirect('llamkay:dashboard')
        
        if request.method == 'POST':
            from apps.jobs.forms import OfertaEmpresaForm
            form = OfertaEmpresaForm(request.POST, request.FILES)
            
            if form.is_valid():
                oferta = form.save(commit=False)
                oferta.id_empleador = usuario
                oferta.save()
                
                messages.success(request, "Oferta publicada exitosamente.")
                return redirect('jobs:mis_trabajos')
        else:
            from apps.jobs.forms import OfertaEmpresaForm
            form = OfertaEmpresaForm()
        
        return render(request, 'jobs/registro/empresa.html', {'form': form})
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')


@login_required
def mis_trabajos(request):
    """Ver trabajos publicados por el empleador"""
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        ofertas_usuario = OfertaUsuario.objects.filter(
            id_empleador=usuario
        ).order_by('-created_at')  # ✅ Cambiado
        
        ofertas_empresa = OfertaEmpresa.objects.filter(
            id_empleador=usuario
        ).order_by('-created_at')  # ✅ Cambiado
        
        context = {
            'ofertas_usuario': ofertas_usuario,
            'ofertas_empresa': ofertas_empresa,
        }
        
        return render(request, 'jobs/mis_trabajos.html', context)
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')


@login_required
def mis_trabajos_ajax(request):
    """Cargar trabajos con AJAX"""
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        ofertas_usuario = OfertaUsuario.objects.filter(
            id_empleador=usuario
        ).values('id', 'titulo', 'estado', 'created_at')  # ✅ Cambiado
        
        ofertas_empresa = OfertaEmpresa.objects.filter(
            id_empleador=usuario
        ).values('id', 'titulo_puesto', 'estado', 'created_at')  # ✅ Cambiado
        
        return JsonResponse({
            'ofertas_usuario': list(ofertas_usuario),
            'ofertas_empresa': list(ofertas_empresa)
        })
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def editar_trabajo(request, oferta_id):
    """Editar una oferta de trabajo"""
    try:
        usuario = Usuario.objects.get(user=request.user)
        
        # Intentar obtener como OfertaUsuario
        oferta = OfertaUsuario.objects.filter(
            id=oferta_id,
            id_empleador=usuario
        ).first()
        
        tipo = 'usuario'
        
        if not oferta:
            # Intentar como OfertaEmpresa
            oferta = OfertaEmpresa.objects.filter(
                id=oferta_id,
                id_empleador=usuario
            ).first()
            tipo = 'empresa'
        
        if not oferta:
            messages.error(request, "Oferta no encontrada.")
            return redirect('jobs:mis_trabajos')
        
        if request.method == 'POST':
            if tipo == 'usuario':
                from apps.jobs.forms import OfertaUsuarioForm
                form = OfertaUsuarioForm(request.POST, request.FILES, instance=oferta)
            else:
                from apps.jobs.forms import OfertaEmpresaForm
                form = OfertaEmpresaForm(request.POST, request.FILES, instance=oferta)
            
            if form.is_valid():
                form.save()
                messages.success(request, "Oferta actualizada correctamente.")
                return redirect('jobs:mis_trabajos')
        else:
            if tipo == 'usuario':
                from apps.jobs.forms import OfertaUsuarioForm
                form = OfertaUsuarioForm(instance=oferta)
            else:
                from apps.jobs.forms import OfertaEmpresaForm
                form = OfertaEmpresaForm(instance=oferta)
        
        context = {
            'form': form,
            'oferta': oferta,
            'tipo': tipo,
        }
        
        return render(request, 'jobs/editar_trabajo.html', context)
        
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no encontrado.")
        return redirect('users:login')


@login_required
@require_POST
def eliminar_trabajo(request, oferta_id):
    """Eliminar (soft delete) una oferta"""
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
        
        # ✅ Soft delete: cambiar estado a cerrada
        oferta.estado = 'cerrada'
        oferta.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Oferta cerrada correctamente'
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
    
    provincias = Provincia.objects.filter(
        id_departamento=id_departamento
    ).values('id_provincia', 'nombre').order_by('nombre')
    
    return JsonResponse(list(provincias), safe=False)


def cargar_distritos(request):
    """Cargar distritos por provincia"""
    id_provincia = request.GET.get('id_provincia')
    
    if not id_provincia:
        return JsonResponse([], safe=False)
    
    distritos = Distrito.objects.filter(
        id_provincia=id_provincia
    ).values('id_distrito', 'nombre').order_by('nombre')
    
    return JsonResponse(list(distritos), safe=False)


def cargar_comunidades(request):
    """Cargar comunidades por distrito"""
    id_distrito = request.GET.get('id_distrito')
    
    if not id_distrito:
        return JsonResponse([], safe=False)
    
    from apps.users.models import Comunidad
    comunidades = Comunidad.objects.filter(
        id_distrito=id_distrito
    ).values('id_comunidad', 'nombre').order_by('nombre')
    
    return JsonResponse(list(comunidades), safe=False)