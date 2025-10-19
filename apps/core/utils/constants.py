# Estados de trabajo
ESTADO_TRABAJO = {
    'PENDIENTE': 'pendiente',
    'EN_PROGRESO': 'en_progreso',
    'COMPLETADO': 'completado',
    'CANCELADO': 'cancelado',
}

# Tipos de usuario
TIPO_USUARIO = {
    'TRABAJADOR': 'trabajador',
    'EMPLEADOR': 'empleador',
    'TRABAJADOR_EMPLEADOR': 'trabajador_empleador',
    'EMPRESA': 'empresa',
}

# Métodos de pago
METODOS_PAGO = {
    'EFECTIVO': 'efectivo',
    'TRANSFERENCIA': 'transferencia',
    'YAPE': 'yape',
    'PLIN': 'plin',
}

# Archivos
MAX_FILE_SIZE_MB = 5
ALLOWED_IMAGE_FORMATS = ['jpg', 'jpeg', 'png', 'gif', 'webp']
ALLOWED_DOCUMENT_FORMATS = ['pdf', 'doc', 'docx']

# Paginación
ITEMS_PER_PAGE = 20