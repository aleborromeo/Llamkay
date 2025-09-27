from .models import OfertaUsuario, OfertaEmpresa
from trabajos.models import GuardarTrabajo, Departamento  # Ajusta si es otro app
from usuarios.models import Usuario

def obtener_trabajos_unificados(limit=None):
    ofertas_usuario = OfertaUsuario.objects.select_related(
        'empleador__profile', 'id_departamento', 'id_provincia', 'id_distrito', 'id_comunidad'
    ).filter(estado='activa')

    ofertas_empresa = OfertaEmpresa.objects.select_related(
        'empleador__profile', 'empleador__empresa', 'id_departamento', 'id_provincia', 'id_distrito', 'id_comunidad'
    ).filter(estado='activa')

    trabajos = []

    for o in ofertas_usuario:
        perfil = getattr(o.empleador, 'perfil', None)
        if perfil and perfil.tipo_usuario == 'empresa' and hasattr(o.empleador, 'empresa'):
            publicado_por = o.empleador.empresa.nombre_empresa
        elif perfil:
            publicado_por = f"{perfil.nombres} {perfil.apellidos}"
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

    # Ordenar por fecha
    trabajos.sort(key=lambda x: x['fecha_registro'], reverse=True)

    if limit:
        return trabajos[:limit]
    return trabajos
