"""
Vista de Contacto - ESTÁTICA (solo muestra info)
"""
from django.shortcuts import render


def contacto(request):
    """
    Página de Contacto
    Solo muestra información - NO guarda en base de datos
    Si quieres un formulario funcional, usa un servicio externo como Formspree
    """
    context = {
        'page_title': 'Contáctanos - Llamkay.pe',
        
        # Información de contacto
        'contacto_info': {
            'email': 'contacto@llamkay.pe',
            'email_soporte': 'soporte@llamkay.pe',
            'telefono': '+51 987 654 321',
            'whatsapp': '51987654321',
            'direccion': 'Av. Principal 123, Lima, Perú',
            'horario': 'Lunes a Viernes: 9:00 AM - 6:00 PM',
        },
        
        # Redes sociales
        'redes_sociales': {
            'facebook': 'https://www.facebook.com/llamkay',
            'instagram': 'https://www.instagram.com/llamkay.pe',
            'tiktok': 'https://www.tiktok.com/@llamkay.pe',
            'linkedin': 'https://www.linkedin.com/company/llamkay',
        },
        
        # Opciones de contacto
        'opciones_contacto': [
            {
                'titulo': 'Soporte Técnico',
                'icono': '🛠️',
                'descripcion': 'Problemas con la plataforma',
                'email': 'soporte@llamkay.pe',
                'tiempo_respuesta': '24 horas'
            },
            {
                'titulo': 'Ventas',
                'icono': '💼',
                'descripcion': 'Planes empresariales',
                'email': 'ventas@llamkay.pe',
                'tiempo_respuesta': '48 horas'
            },
            {
                'titulo': 'Prensa',
                'icono': '📰',
                'descripcion': 'Consultas de medios',
                'email': 'prensa@llamkay.pe',
                'tiempo_respuesta': '72 horas'
            },
        ],
        
        # Mapa (coordenadas para embed de Google Maps)
        'mapa': {
            'latitud': -12.0464,
            'longitud': -77.0428,
            'zoom': 15,
        },
    }
    
    return render(request, 'llamkay/contacto.html', context)
