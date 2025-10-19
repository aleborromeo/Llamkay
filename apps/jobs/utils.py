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
    # ✅ CORREGIDO: 'empleador__profile' en vez de 'empleador__perfil'
    ofertas_usuario = OfertaUsuario.objects.select_related(
        'empleador',
        'empleador__profile',  # ✅ Corregido
        'empleador__empresa',
        'id_departamento', 
        'id_provincia', 
        'id_distrito', 
        'id_comunidad'
    ).filter(estado='activa')

    ofertas_empresa = OfertaEmpresa.objects.select_related(
        'empleador',
        'empleador__profile',  # ✅ Corregido
        'empleador__empresa', 
        'id_departamento', 
        'id_provincia', 
        'id_distrito', 
        'id_comunidad'
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
        profile = getattr(o.empleador, 'profile', None)  # ✅ Corregido
        
        # Determinar quién publicó
        if profile and profile.tipo_usuario == 'empresa' and hasattr(o.empleador, 'empresa'):
            publicado_por = o.empleador.empresa.nombre_empresa
        elif profile:
            publicado_por = f"{profile.nombres} {profile.apellidos}"
        else:
            publicado_por = "Usuario"

        trabajos.append({
            'tipo': 'usuario',
            'id': o.id,
            'titulo': o.titulo,
            'descripcion': o.descripcion,
            'herramientas': o.herramientas,
            'pago': o.pago,
            'foto': o.foto,
            'fecha_registro': o.fecha_registro,
            'fecha_limite': o.fecha_limite,
            'horas_limite': o.horas_limite,
            'rango_salarial': None,
            'experiencia_requerida': None,
            'modalidad_trabajo': None,
            'requisitos_calificaciones': None,
            'beneficios_compensaciones': None,
            'numero_postulantes': None,
            'numero_contacto': o.numero_contacto,
            'id_departamento': o.id_departamento,
            'id_provincia': o.id_provincia,
            'id_distrito': o.id_distrito,
            'id_comunidad': o.id_comunidad,
            'publicado_por': publicado_por,
        })

    # Procesar ofertas de empresas
    for o in ofertas_empresa:
        empresa = getattr(o.empleador, 'empresa', None)
        publicado_por = empresa.nombre_empresa if empresa else "Empresa"

        trabajos.append({
            'tipo': 'empresa',
            'id': o.id,
            'titulo': o.titulo_puesto,
            'descripcion': o.descripcion_puesto,
            'herramientas': None,
            'pago': None,
            'foto': o.foto,
            'fecha_registro': o.fecha_registro,
            'fecha_limite': o.fecha_limite,
            'horas_limite': None,
            'rango_salarial': o.rango_salarial,
            'experiencia_requerida': o.experiencia_requerida,
            'modalidad_trabajo': o.modalidad_trabajo,
            'requisitos_calificaciones': o.requisitos_calificaciones,
            'beneficios_compensaciones': o.beneficios_compensaciones,
            'numero_postulantes': o.numero_postulantes,
            'numero_contacto': o.numero_contacto,
            'id_departamento': o.id_departamento,
            'id_provincia': o.id_provincia,
            'id_distrito': o.id_distrito,
            'id_comunidad': o.id_comunidad,
            'publicado_por': publicado_por,
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
    profile = getattr(oferta.empleador, 'profile', None)  # ✅ Corregido
    empresa = getattr(oferta.empleador, 'empresa', None)
    
    if profile and profile.tipo_usuario == 'empresa' and empresa:
        return empresa.nombre_empresa
    elif profile:
        return f"{profile.nombres} {profile.apellidos}"
    elif empresa:
        return empresa.nombre_empresa
    
    return "Usuario"