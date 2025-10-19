from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


def validate_dni(value):
    """Valida DNI de 8 dígitos"""
    if not value or not value.isdigit() or len(value) != 8:
        raise ValidationError('El DNI debe tener 8 dígitos numéricos')


def validate_ruc(value):
    """Valida RUC de 11 dígitos"""
    if not value or not value.isdigit() or len(value) != 11:
        raise ValidationError('El RUC debe tener 11 dígitos numéricos')


def validate_phone_peru(value):
    """Valida teléfono peruano"""
    import re
    clean = re.sub(r'[^\d]', '', value)
    if not re.match(r'^9\d{8}$', clean):
        raise ValidationError('Teléfono inválido. Debe ser: 9XXXXXXXX')


def validate_file_size(file, max_mb=5):
    """Valida tamaño de archivo"""
    if file and file.size > max_mb * 1024 * 1024:
        raise ValidationError(f'El archivo no debe superar {max_mb}MB')


def tiempo_transcurrido(fecha):
    """
    Calcula el tiempo transcurrido desde una fecha hasta ahora
    Retorna string legible como "hace 2 horas", "hace 3 días"
    """
    if not fecha:
        return ""
    
    ahora = timezone.now()
    diferencia = ahora - fecha
    
    segundos = diferencia.total_seconds()
    
    if segundos < 60:
        return "hace un momento"
    elif segundos < 3600:
        minutos = int(segundos / 60)
        return f"hace {minutos} {'minuto' if minutos == 1 else 'minutos'}"
    elif segundos < 86400:
        horas = int(segundos / 3600)
        return f"hace {horas} {'hora' if horas == 1 else 'horas'}"
    elif segundos < 604800:
        dias = int(segundos / 86400)
        return f"hace {dias} {'día' if dias == 1 else 'días'}"
    elif segundos < 2592000:
        semanas = int(segundos / 604800)
        return f"hace {semanas} {'semana' if semanas == 1 else 'semanas'}"
    elif segundos < 31536000:
        meses = int(segundos / 2592000)
        return f"hace {meses} {'mes' if meses == 1 else 'meses'}"
    else:
        años = int(segundos / 31536000)
        return f"hace {años} {'año' if años == 1 else 'años'}"