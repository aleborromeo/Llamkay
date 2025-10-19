from decimal import Decimal, InvalidOperation


def formatear_moneda(cantidad):
    """Formatea como S/ 1,500.00"""
    if cantidad is None:
        return "S/ 0.00"
    try:
        cantidad = Decimal(str(cantidad))
        return f"S/ {cantidad:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except:
        return "S/ 0.00"


def formatear_dni(dni):
    """Formatea DNI: 1234 5678"""
    if not dni or len(str(dni)) != 8:
        return dni
    dni_str = str(dni)
    return f"{dni_str[:4]} {dni_str[4:]}"


def formatear_telefono(telefono):
    """Formatea teléfono: 987 654 321"""
    if not telefono:
        return telefono
    tel = ''.join(filter(str.isdigit, str(telefono)))
    if len(tel) != 9:
        return telefono
    return f"{tel[:3]} {tel[3:6]} {tel[6:]}"
