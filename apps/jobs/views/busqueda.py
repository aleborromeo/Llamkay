from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse

from apps.jobs.models import OfertaUsuario, OfertaEmpresa, GuardarTrabajo
from apps.users.models import Departamento, Provincia, Distrito, Comunidad, Usuario


def buscar_trabajos(request):
    """Vista principal de búsqueda de trabajos"""
    # Parámetros de búsqueda
    buscar = request.GET.get('buscar', '').strip()
    departamento_id = request.GET.get('departamento_id')
    provincia_id = request.GET.get('provincia_id')
    distrito_id = request.GET.get('distrito_id')
    comunidad_id = request.GET.get('comunidad_id')
    tipo_usuario = request.GET.get('tipo_usuario')  # 'empleador' o 'empresa'
    modalidad = request.GET.get('modalidad')  # Para ofertas de empresa
    
    trabajos = []
    
    # ====== FILTRAR OFERTAS DE USUARIOS ======
    if tipo_usuario in ('', 'empleador'):
        queryset_usuario = OfertaUsuario.objects.select_related(
            'id_empleador',
            'id_empleador__profile',
            'id_categoria',
            'id_departamento',
            'id_provincia',
            'id_distrito',
            'id_comunidad'
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
        if comunidad_id:
            queryset_usuario = queryset_usuario.filter(id_comunidad=comunidad_id)
        
        for oferta in queryset_usuario:
            trabajos.append({
                'tipo': 'usuario',
                'id': oferta.id,
                'titulo': oferta.titulo,
                'descripcion': oferta.descripcion,
                'pago': oferta.pago,
                'modalidad_pago': oferta.get_modalidad_pago_display(),
                'fecha_publicacion': oferta.created_at,
                'fecha_limite': oferta.fecha_limite,
                'urgente': oferta.urgente,
                'empleador': oferta.id_empleador,
                'categoria': oferta.id_categoria.nombre if oferta.id_categoria else '',
                'ubicacion': {
                    'departamento': oferta.id_departamento.nombre if oferta.id_departamento else '',
                    'provincia': oferta.id_provincia.nombre if oferta.id_provincia else '',
                    'distrito': oferta.id_distrito.nombre if oferta.id_distrito else '',
                    'comunidad': oferta.id_comunidad.nombre if oferta.id_comunidad else '',
                },
                'vistas': oferta.vistas,
                'postulaciones': oferta.postulaciones_count,
            })
    
    # ====== FILTRAR OFERTAS DE EMPRESAS ======
    if tipo_usuario in ('', 'empresa'):
        queryset_empresa = OfertaEmpresa.objects.select_related(
            'id_empleador',
            'id_empleador__profile',
            'id_categoria',
            'id_departamento',
            'id_provincia',
            'id_distrito',
            'id_comunidad'
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
        if comunidad_id:
            queryset_empresa = queryset_empresa.filter(id_comunidad=comunidad_id)
        if modalidad:
            queryset_empresa = queryset_empresa.filter(modalidad_trabajo=modalidad)
        
        for oferta in queryset_empresa:
            trabajos.append({
                'tipo': 'empresa',
                'id': oferta.id,
                'titulo': oferta.titulo_puesto,
                'descripcion': oferta.descripcion,
                'rango_salarial': f"{oferta.pago} {oferta.moneda}" if oferta.pago else None,
                'modalidad_pago': oferta.get_modalidad_pago_display(),
                'experiencia_requerida': oferta.experiencia_requerida,
                'fecha_publicacion': oferta.created_at,
                'fecha_limite': oferta.fecha_limite,
                'empleador': oferta.id_empleador,
                'categoria': oferta.id_categoria.nombre if oferta.id_categoria else '',
                'ubicacion': {
                    'departamento': oferta.id_departamento.nombre if oferta.id_departamento else '',
                    'provincia': oferta.id_provincia.nombre if oferta.id_provincia else '',
                    'distrito': oferta.id_distrito.nombre if oferta.id_distrito else '',
                    'comunidad': oferta.id_comunidad.nombre if oferta.id_comunidad else '',
                },
                'vacantes': oferta.vacantes,
                'vistas': oferta.vistas,
                'postulaciones': oferta.postulaciones_count,
            })
    
    # Ordenar por fecha de publicación (más reciente primero)
    trabajos.sort(key=lambda x: x['fecha_publicacion'], reverse=True)
    
    # Obtener trabajos guardados del usuario
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
        except:
            pass
    
    # Datos para filtros
    departamentos = Departamento.objects.all().order_by('nombre')
    
    context = {
        'trabajos': trabajos,
        'departamentos': departamentos,
        'trabajos_guardados_ids': trabajos_guardados_ids,
        'filtros_aplicados': {
            'buscar': buscar,
            'departamento_id': departamento_id,
            'provincia_id': provincia_id,
            'distrito_id': distrito_id,
            'comunidad_id': comunidad_id,
            'tipo_usuario': tipo_usuario,
            'modalidad': modalidad,
        }
    }
    
    return render(request, 'jobs/all_trabajos.html', context)


def detalle_trabajo(request, tipo, trabajo_id):
    """Ver detalle de un trabajo específico"""
    if tipo == 'usuario':
        trabajo = OfertaUsuario.objects.select_related(
            'id_empleador',
            'id_empleador__profile',
            'id_categoria'
        ).get(id=trabajo_id)
        
        # Incrementar vistas
        trabajo.vistas += 1
        trabajo.save(update_fields=['vistas'])
        
    elif tipo == 'empresa':
        trabajo = OfertaEmpresa.objects.select_related(
            'id_empleador',
            'id_empleador__profile',
            'id_categoria'
        ).get(id=trabajo_id)
        
        # Incrementar vistas
        trabajo.vistas += 1
        trabajo.save(update_fields=['vistas'])
    else:
        return JsonResponse({'error': 'Tipo inválido'}, status=400)
    
    # Verificar si ya postuló
    ya_postulo = False
    if request.user.is_authenticated:
        try:
            from apps.jobs.models import Postulacion
            usuario = Usuario.objects.get(user=request.user)
            
            if tipo == 'usuario':
                ya_postulo = Postulacion.objects.filter(
                    id_trabajador=usuario,
                    id_oferta_usuario=trabajo
                ).exists()
            else:
                ya_postulo = Postulacion.objects.filter(
                    id_trabajador=usuario,
                    id_oferta_empresa=trabajo
                ).exists()
        except:
            pass
    
    context = {
        'trabajo': trabajo,
        'tipo': tipo,
        'ya_postulo': ya_postulo,
    }
    
    return render(request, 'jobs/busqueda/detalle.html', context)