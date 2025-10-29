"""
Vistas de Búsqueda y Listado de Trabajos
"""
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from django.http import JsonResponse
from django.core.paginator import Paginator

from apps.jobs.models import OfertaUsuario, OfertaEmpresa, GuardarTrabajo
from apps.jobs.utils import obtener_trabajos_unificados, verificar_ya_postulo
from apps.users.models import Departamento, Provincia, Distrito, Usuario


def buscar_trabajos(request):
    """
    Vista principal de búsqueda de trabajos con filtros
    """
    # Obtener parámetros de búsqueda
    busqueda = request.GET.get('buscar', '').strip()
    departamento_id = request.GET.get('departamento_id')
    provincia_id = request.GET.get('provincia_id')
    distrito_id = request.GET.get('distrito_id')
    tipo_usuario = request.GET.get('tipo_usuario', '')  # 'empleador' o 'empresa'
    categoria_id = request.GET.get('categoria_id')
    page = request.GET.get('page', 1)
    
    # Construir filtros
    filters = {}
    if busqueda:
        filters['busqueda'] = busqueda
    if departamento_id:
        filters['departamento'] = departamento_id
    if provincia_id:
        filters['provincia'] = provincia_id
    if distrito_id:
        filters['distrito'] = distrito_id
    if tipo_usuario:
        filters['tipo'] = tipo_usuario
    if categoria_id:
        filters['categoria'] = categoria_id
    
    # Obtener usuario actual si está autenticado
    usuario_actual = None
    if request.user.is_authenticated:
        try:
            usuario_actual = Usuario.objects.get(user=request.user)
        except Usuario.DoesNotExist:
            pass
    
    # Obtener trabajos unificados
    trabajos = obtener_trabajos_unificados(
        filters=filters,
        usuario_actual=usuario_actual
    )
    
    # Paginar resultados
    paginator = Paginator(trabajos, 12)  # 12 trabajos por página
    trabajos_paginados = paginator.get_page(page)
    
    # Obtener trabajos guardados del usuario
    trabajos_guardados_ids = set()
    if usuario_actual:
        guardados = GuardarTrabajo.objects.filter(id_usuario=usuario_actual)
        for guardado in guardados:
            if guardado.id_oferta_usuario:
                trabajos_guardados_ids.add(f"usuario_{guardado.id_oferta_usuario.id}")
            elif guardado.id_oferta_empresa:
                trabajos_guardados_ids.add(f"empresa_{guardado.id_oferta_empresa.id}")
    
    # Marcar trabajos a los que ya postuló
    for trabajo in trabajos_paginados:
        trabajo['ya_postulo'] = False
        if usuario_actual:
            trabajo['ya_postulo'] = verificar_ya_postulo(
                usuario_actual,
                trabajo['tipo'],
                trabajo['id']
            )
    
    # Datos para filtros
    departamentos = Departamento.objects.all().order_by('nombre')
    provincias = Provincia.objects.none()
    distritos = Distrito.objects.none()
    
    if departamento_id:
        provincias = Provincia.objects.filter(
            id_departamento=departamento_id
        ).order_by('nombre')
    
    if provincia_id:
        distritos = Distrito.objects.filter(
            id_provincia=provincia_id
        ).order_by('nombre')
    
    context = {
        'trabajos': trabajos_paginados,
        'departamentos': departamentos,
        'provincias': provincias,
        'distritos': distritos,
        'trabajos_guardados_ids': trabajos_guardados_ids,
        'filtros': {
            'buscar': busqueda,
            'departamento_id': departamento_id,
            'provincia_id': provincia_id,
            'distrito_id': distrito_id,
            'tipo_usuario': tipo_usuario,
            'categoria_id': categoria_id,
        },
        'total_resultados': len(trabajos),
    }
    
    return render(request, 'jobs/busqueda/lista.html', context)


def all_trabajos(request):
    """
    Vista que muestra todos los trabajos disponibles (alias de buscar_trabajos)
    """
    return buscar_trabajos(request)


def detalle_trabajo(request, tipo, trabajo_id):
    """
    Ver detalle de un trabajo específico
    """
    # Validar tipo
    if tipo not in ['usuario', 'empresa']:
        return JsonResponse({'error': 'Tipo inválido'}, status=400)
    
    # Obtener trabajo según tipo
    if tipo == 'usuario':
        trabajo = get_object_or_404(
            OfertaUsuario.objects.select_related(
                'id_empleador',
                'id_categoria',
                'id_departamento',
                'id_provincia',
                'id_distrito'
            ),
            id=trabajo_id,
            estado='activa'
        )
        # Incrementar vistas
        trabajo.incrementar_vistas()
        
    else:  # empresa
        trabajo = get_object_or_404(
            OfertaEmpresa.objects.select_related(
                'id_empleador',
                'id_categoria',
                'id_departamento',
                'id_provincia',
                'id_distrito'
            ),
            id=trabajo_id,
            estado='activa'
        )
        # Incrementar vistas
        trabajo.incrementar_vistas()
    
    # Verificar si ya postuló
    ya_postulo = False
    es_guardado = False
    es_dueno = False
    
    if request.user.is_authenticated:
        try:
            usuario = Usuario.objects.get(user=request.user)
            
            # Verificar si es el dueño
            es_dueno = (trabajo.id_empleador.id_usuario == usuario.id_usuario)
            
            # Verificar si ya postuló
            ya_postulo = verificar_ya_postulo(usuario, tipo, trabajo_id)
            
            # Verificar si está guardado
            if tipo == 'usuario':
                es_guardado = GuardarTrabajo.objects.filter(
                    id_usuario=usuario,
                    id_oferta_usuario=trabajo
                ).exists()
            else:
                es_guardado = GuardarTrabajo.objects.filter(
                    id_usuario=usuario,
                    id_oferta_empresa=trabajo
                ).exists()
        except Usuario.DoesNotExist:
            pass
    
    # Calcular total de postulaciones
    total_postulaciones = trabajo.postulaciones.filter(
        estado__in=['pendiente', 'en_revision', 'aceptada']
    ).count()
    
    context = {
        'trabajo': trabajo,
        'tipo': tipo,
        'ya_postulo': ya_postulo,
        'es_guardado': es_guardado,
        'es_dueno': es_dueno,
        'total_postulaciones': total_postulaciones,
    }
    
    return render(request, 'jobs/busqueda/detalle.html', context)


def filtrar_trabajos(request):
    """
    Vista AJAX para filtrar trabajos dinámicamente
    """
    if request.method == 'GET':
        # Redirigir a buscar_trabajos con los mismos parámetros
        return buscar_trabajos(request)
    
    # Para peticiones AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        busqueda = request.GET.get('buscar', '').strip()
        departamento_id = request.GET.get('departamento_id')
        provincia_id = request.GET.get('provincia_id')
        distrito_id = request.GET.get('distrito_id')
        tipo_usuario = request.GET.get('tipo_usuario', '')
        
        filters = {}
        if busqueda:
            filters['busqueda'] = busqueda
        if departamento_id:
            filters['departamento'] = departamento_id
        if provincia_id:
            filters['provincia'] = provincia_id
        if distrito_id:
            filters['distrito'] = distrito_id
        if tipo_usuario:
            filters['tipo'] = tipo_usuario
        
        # Obtener usuario actual
        usuario_actual = None
        if request.user.is_authenticated:
            try:
                usuario_actual = Usuario.objects.get(user=request.user)
            except Usuario.DoesNotExist:
                pass
        
        # Obtener trabajos
        trabajos = obtener_trabajos_unificados(
            limit=20,
            filters=filters,
            usuario_actual=usuario_actual
        )
        
        # Formatear respuesta
        trabajos_data = []
        for trabajo in trabajos:
            trabajos_data.append({
                'id': trabajo['id'],
                'tipo': trabajo['tipo'],
                'titulo': trabajo['titulo'],
                'descripcion': trabajo['descripcion'][:150] + '...' if len(trabajo['descripcion']) > 150 else trabajo['descripcion'],
                'pago': str(trabajo['pago']) if trabajo['pago'] else None,
                'moneda': trabajo['moneda'],
                'modalidad_pago': trabajo['modalidad_pago'],
                'empleador': trabajo['empleador']['nombre'],
                'ubicacion': f"{trabajo['ubicacion']['distrito']}, {trabajo['ubicacion']['provincia']}" if trabajo['ubicacion']['distrito'] else trabajo['ubicacion']['provincia'],
                'fecha_publicacion': trabajo['fecha_publicacion'].strftime('%d/%m/%Y'),
                'vistas': trabajo['vistas'],
                'postulaciones': trabajo['postulaciones'],
            })
        
        return JsonResponse({
            'success': True,
            'trabajos': trabajos_data,
            'total': len(trabajos_data)
        })
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)