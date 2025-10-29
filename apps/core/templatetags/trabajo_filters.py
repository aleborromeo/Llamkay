"""
Template filters para manejar objetos OfertaUsuario y OfertaEmpresa
"""
from django import template
from django.urls import reverse

register = template.Library()


@register.filter(name='get_tipo_trabajo')
def get_tipo_trabajo(trabajo):
    """
    Determina el tipo de trabajo basándose en el modelo real
    
    Uso:
    {% load trabajo_filters %}
    {% url 'jobs:detalle_trabajo' tipo=trabajo|get_tipo_trabajo trabajo_id=trabajo|get_id_trabajo %}
    """
    if not trabajo:
        return 'oferta'
    
    # Obtener el nombre de la clase del modelo
    clase = trabajo.__class__.__name__
    
    if clase == 'OfertaUsuario':
        return 'oferta_usuario'
    elif clase == 'OfertaEmpresa':
        return 'oferta_empresa'
    
    # Default
    return 'oferta'


@register.filter(name='get_id_trabajo')
def get_id_trabajo(trabajo):
    """
    Obtiene el ID correcto del trabajo según su tipo
    
    Uso:
    {% url 'jobs:detalle_trabajo' tipo=trabajo|get_tipo_trabajo trabajo_id=trabajo|get_id_trabajo %}
    """
    if not trabajo:
        return 0
    
    # OfertaUsuario usa 'id'
    if hasattr(trabajo, 'id') and trabajo.__class__.__name__ == 'OfertaUsuario':
        return trabajo.id
    
    # OfertaEmpresa usa 'id'
    if hasattr(trabajo, 'id') and trabajo.__class__.__name__ == 'OfertaEmpresa':
        return trabajo.id
    
    return 0


@register.filter(name='get_titulo_trabajo')
def get_titulo_trabajo(trabajo):
    """
    Obtiene el título del trabajo
    OfertaUsuario usa 'titulo'
    OfertaEmpresa usa 'titulo_puesto'
    
    Uso:
    {{ trabajo|get_titulo_trabajo }}
    """
    if not trabajo:
        return 'Trabajo sin título'
    
    # OfertaEmpresa usa titulo_puesto
    if hasattr(trabajo, 'titulo_puesto') and trabajo.titulo_puesto:
        return trabajo.titulo_puesto
    
    # OfertaUsuario usa titulo
    if hasattr(trabajo, 'titulo') and trabajo.titulo:
        return trabajo.titulo
    
    return 'Trabajo sin título'


@register.filter(name='get_empleador_trabajo')
def get_empleador_trabajo(trabajo):
    """
    Obtiene el empleador del trabajo
    Ambos modelos usan 'id_empleador'
    
    Uso:
    {% with empleador=trabajo|get_empleador_trabajo %}
        {{ empleador.nombres }} {{ empleador.apellidos }}
    {% endwith %}
    """
    if not trabajo:
        return None
    
    # Ambos modelos tienen id_empleador
    if hasattr(trabajo, 'id_empleador'):
        return trabajo.id_empleador
    
    return None


@register.filter(name='get_pago_trabajo')
def get_pago_trabajo(trabajo):
    """
    Obtiene el pago del trabajo
    Ambos modelos usan 'pago'
    
    Uso:
    {{ trabajo|get_pago_trabajo }}
    """
    if not trabajo:
        return None
    
    if hasattr(trabajo, 'pago') and trabajo.pago:
        return trabajo.pago
    
    return None


@register.filter(name='get_descripcion_trabajo')
def get_descripcion_trabajo(trabajo):
    """
    Obtiene la descripción del trabajo
    Ambos modelos usan 'descripcion'
    
    Uso:
    {{ trabajo|get_descripcion_trabajo|truncatewords:20 }}
    """
    if not trabajo:
        return ''
    
    if hasattr(trabajo, 'descripcion') and trabajo.descripcion:
        return trabajo.descripcion
    
    return ''


@register.filter(name='get_distrito_trabajo')
def get_distrito_trabajo(trabajo):
    """
    Obtiene el distrito del trabajo
    Ambos modelos usan 'id_distrito'
    
    Uso:
    {{ trabajo|get_distrito_trabajo }}
    """
    if not trabajo:
        return None
    
    if hasattr(trabajo, 'id_distrito') and trabajo.id_distrito:
        return trabajo.id_distrito
    
    return None


@register.filter(name='is_urgente')
def is_urgente(trabajo):
    """
    Verifica si el trabajo es urgente
    Solo OfertaUsuario tiene campo 'urgente'
    
    Uso:
    {% if trabajo|is_urgente %}
        <span class="badge urgent">Urgente</span>
    {% endif %}
    """
    if not trabajo:
        return False
    
    # Solo OfertaUsuario tiene campo urgente
    if hasattr(trabajo, 'urgente'):
        return trabajo.urgente
    
    return False


@register.filter(name='get_created_at')
def get_created_at(trabajo):
    """
    Obtiene la fecha de creación
    Ambos modelos usan 'created_at'
    
    Uso:
    {{ trabajo|get_created_at|timesince }}
    """
    if not trabajo:
        return None
    
    if hasattr(trabajo, 'created_at'):
        return trabajo.created_at
    
    return None


@register.simple_tag
def url_detalle_trabajo(trabajo):
    """
    Genera la URL completa para el detalle del trabajo
    
    Uso:
    {% load trabajo_filters %}
    <a href="{% url_detalle_trabajo trabajo %}">Ver detalle</a>
    """
    if not trabajo:
        return '#'
    
    tipo = get_tipo_trabajo(trabajo)
    trabajo_id = get_id_trabajo(trabajo)
    
    try:
        return reverse('jobs:detalle_trabajo', kwargs={
            'tipo': tipo,
            'trabajo_id': trabajo_id
        })
    except:
        return '#'


@register.simple_tag
def url_postular_trabajo(trabajo):
    """
    Genera la URL para postular al trabajo
    
    Uso:
    {% load trabajo_filters %}
    <a href="{% url_postular_trabajo trabajo %}">Aplicar</a>
    """
    if not trabajo:
        return '#'
    
    tipo = get_tipo_trabajo(trabajo)
    oferta_id = get_id_trabajo(trabajo)
    
    try:
        return reverse('jobs:postular_trabajo', kwargs={
            'tipo': tipo,
            'oferta_id': oferta_id
        })
    except:
        return '#'