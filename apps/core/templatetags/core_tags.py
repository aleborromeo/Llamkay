from django import template
from apps.core.utils.formatters import formatear_moneda, formatear_dni, formatear_telefono
from apps.core.utils.helpers import tiempo_transcurrido

register = template.Library()


@register.filter
def moneda(value):
    """{{ precio|moneda }}"""
    return formatear_moneda(value)


@register.filter
def dni(value):
    """{{ usuario.dni|dni }}"""
    return formatear_dni(value)


@register.filter
def telefono(value):
    """{{ usuario.telefono|telefono }}"""
    return formatear_telefono(value)


@register.filter
def tiempo(value):
    """{{ fecha|tiempo }}"""
    return tiempo_transcurrido(value)


@register.simple_tag
def settings_value(name, default=''):
    """{% settings_value 'SITE_NAME' %}"""
    from django.conf import settings
    return getattr(settings, name, default)
