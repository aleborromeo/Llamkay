"""
Vista de "Nosotros"
"""
from django.shortcuts import render


def nosotros(request):
    """
    Página "Sobre Nosotros"
    Información de la empresa, misión, visión, equipo
    """
    context = {
        'page_title': 'Sobre Nosotros - Llamkay.pe',
        
        # Información de la empresa
        'mision': 'Conectar talento peruano con oportunidades laborales de calidad',
        'vision': 'Ser la plataforma líder de empleo en Perú para el 2025',
        
        # Valores
        'valores': [
            {
                'titulo': 'Confianza',
                'icono': '🤝',
                'descripcion': 'Verificamos cada perfil para garantizar seguridad'
            },
            {
                'titulo': 'Transparencia',
                'icono': '💎',
                'descripcion': 'Información clara y veraz en cada publicación'
            },
            {
                'titulo': 'Calidad',
                'icono': '⭐',
                'descripcion': 'Solo los mejores profesionales en nuestra plataforma'
            },
            {
                'titulo': 'Innovación',
                'icono': '🚀',
                'descripcion': 'Tecnología de punta para mejorar tu experiencia'
            },
        ],
        
    }
    
    return render(request, 'llamkay/nosotros.html', context)