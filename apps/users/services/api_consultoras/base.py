"""
Interfaz Base para Consultores de API
Implementa el Principio Open/Closed (OCP)
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class ConsultorAPIBase(ABC):
    """
    Clase abstracta para servicios de consulta externa
    Permite agregar nuevos consultores sin modificar código existente
    """
    
    def __init__(self, token: str):
        """
        Constructor base con el token de autenticación
        
        Args:
            token: Token de API para autenticación
        """
        self.token = token
        self.timeout = 10  # Timeout por defecto
    
    @abstractmethod
    def consultar(self, identificador: str) -> Dict[str, Any]:
        """
        Realiza la consulta al servicio externo
        
        Args:
            identificador: DNI, RUC u otro identificador
            
        Returns:
            Dict con la respuesta procesada
        """
        pass
    
    @abstractmethod
    def validar_identificador(self, identificador: str) -> bool:
        """
        Valida el formato del identificador
        
        Args:
            identificador: Identificador a validar
            
        Returns:
            True si es válido, False en caso contrario
        """
        pass
    
    def _construir_headers(self) -> Dict[str, str]:
        """
        Construye los headers de autenticación
        Método protegido compartido por todos los consultores
        
        Returns:
            Dict con los headers
        """
        return {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/json"
        }
    
    def _procesar_error(self, status_code: int, mensaje: str = None) -> Dict[str, Any]:
        """
        Procesa y formatea errores de manera consistente
        
        Args:
            status_code: Código de estado HTTP
            mensaje: Mensaje personalizado de error
            
        Returns:
            Dict con información del error
        """
        errores = {
            401: 'Token de API inválido. Contacta al administrador.',
            404: 'Información no encontrada.',
            429: 'Demasiadas solicitudes. Intenta más tarde.',
            500: 'Error en el servidor externo.',
            503: 'Servicio no disponible temporalmente.',
        }
        
        mensaje_error = mensaje or errores.get(status_code, f'Error HTTP {status_code}')
        
        return {
            'success': False,
            'error': mensaje_error,
            'status_code': status_code
        }