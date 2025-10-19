from django.core.exceptions import ValidationError


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
