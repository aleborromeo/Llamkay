"""
Utilidades para el módulo de trabajos - CORREGIDO
"""
from .models import OfertaUsuario, OfertaEmpresa


def obtener_trabajos_unificados(limit=None, filters=None):
    """
    Combina ofertas de usuarios y empresas en una lista unificada.
    
    Args:
        limit (int, optional): Número máximo de trabajos a retornar
        filters (dict, optional): Filtros adicionales a aplicar
    
    Returns:
        list: Lista de diccionarios con información unificada de trabajos
    """
    # Query base con select_related para optimizar consultas
    ofertas_usuario = OfertaUsuario.objects.select_related(
        'id_empleador',
        'id_categoria', 
        'id_departamento', 
        'id_provincia', 
        'id_distrito'
    ).filter(estado='activa')

    ofertas_empresa = OfertaEmpresa.objects.select_related(
        'id_empleador',
        'id_categoria', 
        'id_departamento', 
        'id_provincia', 
        'id_distrito'
    ).filter(estado='activa')

    # Aplicar filtros si existen
    if filters:
        if 'departamento' in filters:
            ofertas_usuario = ofertas_usuario.filter(id_departamento=filters['departamento'])
            ofertas_empresa = ofertas_empresa.filter(id_departamento=filters['departamento'])
        if 'provincia' in filters:
            ofertas_usuario = ofertas_usuario.filter(id_provincia=filters['provincia'])
            ofertas_empresa = ofertas_empresa.filter(id_provincia=filters['provincia'])

    trabajos = []

    # Procesar ofertas de usuarios
    for o in ofertas_usuario:
        # ✅ Obtener nombre del publicador
        empleador = o.id_empleador
        if hasattr(empleador, 'empresa') and empleador.empresa:
            publicado_por = empleador.empresa.nombre_empresa
        else:
            # ✅ Asumiendo que Usuario tiene estos campos directamente
            # Ajusta según tu modelo real de Usuario
            publicado_por = f"{empleador.nombres} {empleador.apellidos}" if hasattr(empleador, 'nombres') else "Usuario"

        trabajos.append({
            'tipo': 'usuario',
            'id': o.id,
            'titulo': o.titulo,
            'descripcion': o.descripcion,
            'pago': o.pago,
            'moneda': o.moneda,
            'modalidad_pago': o.get_modalidad_pago_display(),
            'fecha_registro': o.created_at,  # ✅ Cambiado
            'fecha_limite': o.fecha_limite,
            'fecha_inicio_estimada': o.fecha_inicio_estimada,
            'urgente': o.urgente,
            'direccion_detalle': o.direccion_detalle,
            'id_departamento': o.id_departamento,
            'id_provincia': o.id_provincia,
            'id_distrito': o.id_distrito,
            'publicado_por': publicado_por,
            'categoria': o.id_categoria.nombre if o.id_categoria else None,
            'vistas': o.vistas,
        })

    # Procesar ofertas de empresas
    for o in ofertas_empresa:
        empleador = o.id_empleador
        if hasattr(empleador, 'empresa') and empleador.empresa:
            publicado_por = empleador.empresa.nombre_empresa
        else:
            publicado_por = "Empresa"

        trabajos.append({
            'tipo': 'empresa',
            'id': o.id,
            'titulo': o.titulo_puesto,
            'descripcion': o.descripcion,
            'pago': o.pago,
            'moneda': o.moneda,
            'modalidad_pago': o.get_modalidad_pago_display(),
            'experiencia_requerida': o.experiencia_requerida,
            'vacantes': o.vacantes,
            'fecha_registro': o.created_at,  # ✅ Cambiado
            'id_departamento': o.id_departamento,
            'id_provincia': o.id_provincia,
            'id_distrito': o.id_distrito,
            'publicado_por': publicado_por,
            'categoria': o.id_categoria.nombre if o.id_categoria else None,
            'vistas': o.vistas,
        })

    # Ordenar por fecha de registro (más recientes primero)
    trabajos.sort(key=lambda x: x['fecha_registro'], reverse=True)

    # Aplicar límite si existe
    if limit:
        return trabajos[:limit]
    
    return trabajos


def obtener_publicador_nombre(oferta):
    """
    Obtiene el nombre del publicador de una oferta.
    
    Args:
        oferta: Instancia de OfertaUsuario u OfertaEmpresa
    
    Returns:
        str: Nombre del publicador
    """
    empleador = oferta.id_empleador
    
    # Intentar obtener empresa primero
    if hasattr(empleador, 'empresa') and empleador.empresa:
        return empleador.empresa.nombre_empresa
    
    # Si no hay empresa, usar nombre del usuario
    if hasattr(empleador, 'nombres') and hasattr(empleador, 'apellidos'):
        return f"{empleador.nombres} {empleador.apellidos}"
    
    # Fallback
    return "Usuario"