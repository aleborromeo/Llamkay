"""
Utilidades para el módulo de trabajos - OPTIMIZADO
"""
from django.db.models import Q, Count, Prefetch
from .models import OfertaUsuario, OfertaEmpresa, Postulacion


def obtener_trabajos_unificados(limit=None, filters=None, usuario_actual=None):
    """
    Combina ofertas de usuarios y empresas en una lista unificada.
    
    Args:
        limit (int): Número máximo de trabajos a retornar
        filters (dict): Filtros a aplicar (departamento, provincia, distrito, categoria, busqueda)
        usuario_actual (Usuario): Usuario actual para filtrar trabajos propios
    
    Returns:
        list: Lista de diccionarios con información unificada de trabajos
    """
    # Query base optimizada con select_related
    queryset_usuario = OfertaUsuario.objects.select_related(
        'id_empleador',
        'id_categoria', 
        'id_departamento', 
        'id_provincia', 
        'id_distrito'
    ).filter(estado='activa')

    queryset_empresa = OfertaEmpresa.objects.select_related(
        'id_empleador',
        'id_categoria', 
        'id_departamento', 
        'id_provincia', 
        'id_distrito'
    ).filter(estado='activa')

    # Excluir trabajos propios si hay usuario autenticado
    if usuario_actual:
        queryset_usuario = queryset_usuario.exclude(id_empleador=usuario_actual)
        queryset_empresa = queryset_empresa.exclude(id_empleador=usuario_actual)

    # Aplicar filtros si existen
    if filters:
        if 'busqueda' in filters and filters['busqueda']:
            busqueda = filters['busqueda']
            queryset_usuario = queryset_usuario.filter(
                Q(titulo__icontains=busqueda) |
                Q(descripcion__icontains=busqueda) |
                Q(id_categoria__nombre__icontains=busqueda)
            )
            queryset_empresa = queryset_empresa.filter(
                Q(titulo_puesto__icontains=busqueda) |
                Q(descripcion__icontains=busqueda) |
                Q(id_categoria__nombre__icontains=busqueda)
            )
        
        if 'departamento' in filters and filters['departamento']:
            queryset_usuario = queryset_usuario.filter(id_departamento=filters['departamento'])
            queryset_empresa = queryset_empresa.filter(id_departamento=filters['departamento'])
        
        if 'provincia' in filters and filters['provincia']:
            queryset_usuario = queryset_usuario.filter(id_provincia=filters['provincia'])
            queryset_empresa = queryset_empresa.filter(id_provincia=filters['provincia'])
        
        if 'distrito' in filters and filters['distrito']:
            queryset_usuario = queryset_usuario.filter(id_distrito=filters['distrito'])
            queryset_empresa = queryset_empresa.filter(id_distrito=filters['distrito'])
        
        if 'categoria' in filters and filters['categoria']:
            queryset_usuario = queryset_usuario.filter(id_categoria=filters['categoria'])
            queryset_empresa = queryset_empresa.filter(id_categoria=filters['categoria'])
        
        if 'tipo' in filters:
            if filters['tipo'] == 'empleador':
                queryset_empresa = OfertaEmpresa.objects.none()
            elif filters['tipo'] == 'empresa':
                queryset_usuario = OfertaUsuario.objects.none()

    # Anotar con conteo de postulaciones
    queryset_usuario = queryset_usuario.annotate(
        postulaciones_count=Count('postulaciones', filter=Q(postulaciones__estado='pendiente'))
    )
    queryset_empresa = queryset_empresa.annotate(
        postulaciones_count=Count('postulaciones', filter=Q(postulaciones__estado='pendiente'))
    )

    trabajos = []

    # Procesar ofertas de usuarios
    for oferta in queryset_usuario:
        trabajos.append({
            'tipo': 'usuario',
            'id': oferta.id,
            'titulo': oferta.titulo,
            'descripcion': oferta.descripcion,
            'pago': oferta.pago,
            'moneda': oferta.moneda,
            'modalidad_pago': oferta.get_modalidad_pago_display(),
            'fecha_publicacion': oferta.created_at,
            'fecha_limite': oferta.fecha_limite,
            'fecha_inicio_estimada': oferta.fecha_inicio_estimada,
            'urgente': oferta.urgente,
            'direccion_detalle': oferta.direccion_detalle,
            'empleador': {
                'id': oferta.id_empleador.id_usuario,
                'nombre': oferta.id_empleador.nombre_completo,
                'email': oferta.id_empleador.email if hasattr(oferta.id_empleador, 'email') else None,
            },
            'ubicacion': {
                'departamento': oferta.id_departamento.nombre if oferta.id_departamento else None,
                'provincia': oferta.id_provincia.nombre if oferta.id_provincia else None,
                'distrito': oferta.id_distrito.nombre if oferta.id_distrito else None,
            },
            'categoria': {
                'id': oferta.id_categoria.id_categoria,
                'nombre': oferta.id_categoria.nombre,
                'icono': oferta.id_categoria.icono if hasattr(oferta.id_categoria, 'icono') else None,
            } if oferta.id_categoria else None,
            'vistas': oferta.vistas,
            'postulaciones': oferta.postulaciones_count,
        })

    # Procesar ofertas de empresas
    for oferta in queryset_empresa:
        trabajos.append({
            'tipo': 'empresa',
            'id': oferta.id,
            'titulo': oferta.titulo_puesto,
            'descripcion': oferta.descripcion,
            'pago': oferta.pago,
            'moneda': oferta.moneda,
            'modalidad_pago': oferta.get_modalidad_pago_display(),
            'experiencia_requerida': oferta.experiencia_requerida,
            'vacantes': oferta.vacantes,
            'fecha_publicacion': oferta.created_at,
            'empleador': {
                'id': oferta.id_empleador.id_usuario,
                'nombre': oferta.id_empleador.nombre_completo,
                'email': oferta.id_empleador.email if hasattr(oferta.id_empleador, 'email') else None,
            },
            'ubicacion': {
                'departamento': oferta.id_departamento.nombre if oferta.id_departamento else None,
                'provincia': oferta.id_provincia.nombre if oferta.id_provincia else None,
                'distrito': oferta.id_distrito.nombre if oferta.id_distrito else None,
            },
            'categoria': {
                'id': oferta.id_categoria.id_categoria,
                'nombre': oferta.id_categoria.nombre,
                'icono': oferta.id_categoria.icono if hasattr(oferta.id_categoria, 'icono') else None,
            } if oferta.id_categoria else None,
            'vistas': oferta.vistas,
            'postulaciones': oferta.postulaciones_count,
        })

    # Ordenar por fecha de publicación (más recientes primero)
    trabajos.sort(key=lambda x: x['fecha_publicacion'], reverse=True)

    # Aplicar límite si existe
    if limit:
        return trabajos[:limit]
    
    return trabajos


def verificar_ya_postulo(usuario, tipo_oferta, oferta_id):
    """
    Verifica si un usuario ya postuló a una oferta específica.
    
    Args:
        usuario (Usuario): Usuario a verificar
        tipo_oferta (str): 'usuario' o 'empresa'
        oferta_id (int): ID de la oferta
    
    Returns:
        bool: True si ya postuló, False en caso contrario
    """
    if tipo_oferta == 'usuario':
        return Postulacion.objects.filter(
            id_trabajador=usuario,
            id_oferta_usuario_id=oferta_id
        ).exists()
    elif tipo_oferta == 'empresa':
        return Postulacion.objects.filter(
            id_trabajador=usuario,
            id_oferta_empresa_id=oferta_id
        ).exists()
    return False


def obtener_postulaciones_usuario(usuario, estado=None):
    """
    Obtiene todas las postulaciones de un usuario.
    
    Args:
        usuario (Usuario): Usuario
        estado (str): Filtrar por estado (opcional)
    
    Returns:
        QuerySet: Postulaciones del usuario
    """
    queryset = Postulacion.objects.filter(
        id_trabajador=usuario
    ).select_related(
        'id_oferta_usuario',
        'id_oferta_usuario__id_empleador',
        'id_oferta_usuario__id_categoria',
        'id_oferta_empresa',
        'id_oferta_empresa__id_empleador',
        'id_oferta_empresa__id_categoria',
    ).order_by('-created_at')
    
    if estado:
        queryset = queryset.filter(estado=estado)
    
    return queryset


def obtener_postulaciones_empleador(usuario, estado=None):
    """
    Obtiene todas las postulaciones recibidas por un empleador.
    
    Args:
        usuario (Usuario): Empleador
        estado (str): Filtrar por estado (opcional)
    
    Returns:
        QuerySet: Postulaciones recibidas
    """
    queryset = Postulacion.objects.filter(
        Q(id_oferta_usuario__id_empleador=usuario) |
        Q(id_oferta_empresa__id_empleador=usuario)
    ).select_related(
        'id_trabajador',
        'id_oferta_usuario',
        'id_oferta_empresa',
    ).order_by('-created_at')
    
    if estado:
        queryset = queryset.filter(estado=estado)
    
    return queryset


def formatear_postulacion(postulacion):
    """
    Formatea una postulación para mostrar en templates.
    
    Args:
        postulacion (Postulacion): Instancia de Postulacion
    
    Returns:
        dict: Datos formateados
    """
    oferta = postulacion.oferta
    tipo = postulacion.tipo_oferta
    
    return {
        'id': postulacion.id_postulacion,
        'tipo': tipo,
        'titulo': oferta.titulo if tipo == 'usuario' else oferta.titulo_puesto,
        'descripcion': oferta.descripcion,
        'empleador': {
            'id': oferta.id_empleador.id_usuario,
            'nombre': oferta.id_empleador.nombre_completo,
        },
        'trabajador': {
            'id': postulacion.id_trabajador.id_usuario,
            'nombre': postulacion.id_trabajador.nombre_completo,
        },
        'mensaje': postulacion.mensaje,
        'pretension_salarial': postulacion.pretension_salarial,
        'disponibilidad_inmediata': postulacion.disponibilidad_inmediata,
        'estado': postulacion.estado,
        'estado_display': postulacion.get_estado_display(),
        'leida': postulacion.leida,
        'fecha_postulacion': postulacion.created_at,
        'oferta_id': oferta.id,
    }


def obtener_estadisticas_empleador(usuario):
    """
    Calcula estadísticas para el dashboard del empleador.
    
    Args:
        usuario (Usuario): Empleador
    
    Returns:
        dict: Estadísticas calculadas
    """
    ofertas_usuario = OfertaUsuario.objects.filter(id_empleador=usuario)
    ofertas_empresa = OfertaEmpresa.objects.filter(id_empleador=usuario)
    
    return {
        'total_ofertas_usuario': ofertas_usuario.count(),
        'total_ofertas_empresa': ofertas_empresa.count(),
        'ofertas_activas': ofertas_usuario.filter(estado='activa').count() + 
                          ofertas_empresa.filter(estado='activa').count(),
        'total_postulaciones': Postulacion.objects.filter(
            Q(id_oferta_usuario__id_empleador=usuario) |
            Q(id_oferta_empresa__id_empleador=usuario)
        ).count(),
        'postulaciones_pendientes': Postulacion.objects.filter(
            Q(id_oferta_usuario__id_empleador=usuario) |
            Q(id_oferta_empresa__id_empleador=usuario),
            estado='pendiente'
        ).count(),
        'vistas_totales': ofertas_usuario.aggregate(total=Count('vistas'))['total'] or 0 +
                         ofertas_empresa.aggregate(total=Count('vistas'))['total'] or 0,
    }


def obtener_estadisticas_trabajador(usuario):
    """
    Calcula estadísticas para el dashboard del trabajador.
    
    Args:
        usuario (Usuario): Trabajador
    
    Returns:
        dict: Estadísticas calculadas
    """
    postulaciones = Postulacion.objects.filter(id_trabajador=usuario)
    
    return {
        'total_postulaciones': postulaciones.count(),
        'postulaciones_pendientes': postulaciones.filter(estado='pendiente').count(),
        'postulaciones_aceptadas': postulaciones.filter(estado='aceptada').count(),
        'postulaciones_rechazadas': postulaciones.filter(estado='rechazada').count(),
        'tasa_aceptacion': calcular_tasa_aceptacion(postulaciones),
    }


def calcular_tasa_aceptacion(postulaciones):
    """
    Calcula la tasa de aceptación de postulaciones.
    
    Args:
        postulaciones (QuerySet): QuerySet de postulaciones
    
    Returns:
        float: Tasa de aceptación en porcentaje
    """
    total = postulaciones.count()
    if total == 0:
        return 0.0
    
    aceptadas = postulaciones.filter(estado='aceptada').count()
    return round((aceptadas / total) * 100, 1)