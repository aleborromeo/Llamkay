"""
Vista del Landing Page (Home)
"""
from django.shortcuts import render


def home(request):
    """
    Página principal del sitio
    Muestra estadísticas, trabajos destacados, etc.
    """
    context = {
        'page_title': 'Llamkay.pe - Encuentra trabajo o contrata profesionales',
        
        # Estadísticas (hardcoded - datos estáticos)
        'estadisticas': {
            'total_trabajadores': 1250,
            'total_empleadores': 890,
            'trabajos_publicados': 3400,
            'trabajos_completados': 2100,
        },
        
        # Categorías populares
        'categorias_populares': [
            {'nombre': 'Carpintería', 'icon': '🔨', 'trabajos': 156},
            {'nombre': 'Electricidad', 'icon': '💡', 'trabajos': 143},
            {'nombre': 'Plomería', 'icon': '🔧', 'trabajos': 128},
            {'nombre': 'Albañilería', 'icon': '🧱', 'trabajos': 201},
            {'nombre': 'Jardinería', 'icon': '🌱', 'trabajos': 89},
            {'nombre': 'Limpieza', 'icon': '🧹', 'trabajos': 167},
        ],
        
        # Testimonios
        'testimonios': [
            {
                'nombre': 'Juan Pérez',
                'foto': 'testimonios/juan.jpg',
                'testimonio': 'Conseguí trabajo en menos de una semana. ¡Excelente plataforma!',
                'rating': 5
            },
            {
                'nombre': 'María López',
                'foto': 'testimonios/maria.jpg',
                'testimonio': 'Encontré al trabajador perfecto para mi proyecto. Muy recomendado.',
                'rating': 5
            },
            {
                'nombre': 'Carlos Ruiz',
                'foto': 'testimonios/carlos.jpg',
                'testimonio': 'La mejor plataforma para ofrecer mis servicios como carpintero.',
                'rating': 5
            },
        ],
    }
    
    return render(request, 'llamkay/index.html', context)