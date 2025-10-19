"""
Vistas de páginas legales (estáticas)
"""
from django.shortcuts import render


def terminos(request):
    """
    Términos y Condiciones de Uso
    Página completamente estática - contenido en el template
    """
    context = {
        'page_title': 'Términos y Condiciones - Llamkay.pe',
        'ultima_actualizacion': '15 de enero de 2025',
    }
    return render(request, 'llamkay/terminos.html', context)


def privacidad(request):
    """
    Política de Privacidad
    Página completamente estática - contenido en el template
    """
    context = {
        'page_title': 'Política de Privacidad - Llamkay.pe',
        'ultima_actualizacion': '15 de enero de 2025',
    }
    return render(request, 'llamkay/privacidad.html', context)
