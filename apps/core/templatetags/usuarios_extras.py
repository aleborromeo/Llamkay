from django import template

register = template.Library()

@register.filter
def usuario(value):
    try:
        return value.get_full_name() or value.username
    except AttributeError:
        return str(value)
