def site_info(request):
    """Variables globales para todos los templates"""
    return {
        'SITE_NAME': 'Llamkay.pe',
        'SITE_VERSION': '1.0.0',
        'SUPPORT_EMAIL': 'soporte@llamkay.pe',
        'SUPPORT_PHONE': '+51 987 654 321',
    }


def user_data(request):
    """Datos del usuario actual"""
    if request.user.is_authenticated:
        return {
            'user_full_name': request.user.get_full_name() or request.user.username,
            'user_initials': f"{request.user.first_name[:1]}{request.user.last_name[:1]}".upper(),
        }
    return {}
