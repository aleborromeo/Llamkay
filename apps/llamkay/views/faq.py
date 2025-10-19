"""
Vista de Preguntas Frecuentes (FAQ) - ESTÁTICA
"""
from django.shortcuts import render


def preguntas_frecuentes(request):
    """
    Preguntas Frecuentes
    Datos hardcoded en el código (sin base de datos)
    """
    context = {
        'page_title': 'Preguntas Frecuentes - Llamkay.pe',
        
        # Preguntas organizadas por categoría
        'categorias': [
            {
                'nombre': 'General',
                'icono': '❓',
                'preguntas': [
                    {
                        'pregunta': '¿Qué es Llamkay?',
                        'respuesta': 'Llamkay es una plataforma que conecta trabajadores independientes con empleadores que necesitan sus servicios.'
                    },
                    {
                        'pregunta': '¿Es gratis usar Llamkay?',
                        'respuesta': 'Sí, registrarte y buscar trabajos es completamente gratis. Solo cobramos una comisión cuando completas un trabajo exitosamente.'
                    },
                    {
                        'pregunta': '¿En qué ciudades está disponible?',
                        'respuesta': 'Llamkay está disponible en todo el Perú, con mayor presencia en Lima, Arequipa, Cusco y Trujillo.'
                    },
                ],
            },
            {
                'nombre': 'Para Trabajadores',
                'icono': '🔨',
                'preguntas': [
                    {
                        'pregunta': '¿Cómo me registro como trabajador?',
                        'respuesta': 'Haz clic en "Registrarse", selecciona "Buscar trabajo" y completa tu perfil con tus habilidades y experiencia.'
                    },
                    {
                        'pregunta': '¿Necesito tener experiencia previa?',
                        'respuesta': 'No necesariamente. Aceptamos trabajadores de todos los niveles, desde principiantes hasta expertos.'
                    },
                    {
                        'pregunta': '¿Cómo me pagan?',
                        'respuesta': 'El pago se coordina directamente con el empleador. Puedes recibir pagos en efectivo, transferencia bancaria o billeteras digitales como Yape o Plin.'
                    },
                    {
                        'pregunta': '¿Puedo ofrecer múltiples servicios?',
                        'respuesta': 'Sí, puedes agregar todas las habilidades que tengas en tu perfil.'
                    },
                ],
            },
            {
                'nombre': 'Para Empleadores',
                'icono': '💼',
                'preguntas': [
                    {
                        'pregunta': '¿Cómo publico un trabajo?',
                        'respuesta': 'Regístrate como empleador, ve a "Publicar trabajo" y completa los detalles de lo que necesitas.'
                    },
                    {
                        'pregunta': '¿Cuánto cuesta publicar?',
                        'respuesta': 'Publicar trabajos es gratis. Solo pagas al trabajador que contrates según lo acordado.'
                    },
                    {
                        'pregunta': '¿Cómo elijo al mejor trabajador?',
                        'respuesta': 'Revisa los perfiles, calificaciones, certificaciones y trabajos anteriores. También puedes chatear con ellos antes de contratar.'
                    },
                    {
                        'pregunta': '¿Qué pasa si no estoy satisfecho con el trabajo?',
                        'respuesta': 'Contamos con un sistema de mediación. Contacta a nuestro soporte para resolver cualquier inconveniente.'
                    },
                ],
            },
            {
                'nombre': 'Seguridad y Confianza',
                'icono': '🔒',
                'preguntas': [
                    {
                        'pregunta': '¿Cómo verifican a los trabajadores?',
                        'respuesta': 'Todos los trabajadores deben subir sus antecedentes penales y verificar su identidad con DNI.'
                    },
                    {
                        'pregunta': '¿Qué hago si tengo un problema?',
                        'respuesta': 'Contacta inmediatamente a nuestro equipo de soporte a través del chat en vivo o email: soporte@llamkay.pe'
                    },
                    {
                        'pregunta': '¿Mis datos están seguros?',
                        'respuesta': 'Sí, usamos encriptación y seguimos las mejores prácticas de seguridad para proteger tu información.'
                    },
                ],
            },
            {
                'nombre': 'Pagos y Comisiones',
                'icono': '💰',
                'preguntas': [
                    {
                        'pregunta': '¿Cuánto cobran de comisión?',
                        'respuesta': 'Cobramos una comisión del 10% sobre el valor del trabajo completado.'
                    },
                    {
                        'pregunta': '¿Cuándo se cobra la comisión?',
                        'respuesta': 'La comisión se cobra únicamente cuando el trabajo se marca como completado y ambas partes están satisfechas.'
                    },
                    {
                        'pregunta': '¿Qué métodos de pago aceptan?',
                        'respuesta': 'Aceptamos tarjetas de crédito/débito, transferencias bancarias, Yape y Plin.'
                    },
                ],
            },
        ],
    }
    
    return render(request, 'llamkay/faq.html', context)
