"""
Consultor de API SUNAT (RUC)
Usa apis.net.pe con token JWT + fallback
"""

import requests
from typing import Dict, Any

from .base import ConsultorAPIBase


class ConsultorSUNAT(ConsultorAPIBase):
    """
    Consultor para verificación de RUC en SUNAT
    """
    
    def __init__(self, token: str = None):
        super().__init__(token or "")
        self.url_base = "https://api.apis.net.pe/v2/sunat/ruc"
    
    def validar_identificador(self, ruc: str) -> bool:
        """Valida que el RUC tenga formato correcto"""
        if not ruc:
            return False
        return len(ruc) == 11 and ruc.isdigit()
    
    def consultar(self, ruc: str) -> Dict[str, Any]:
        """Consulta información de un RUC"""
        if not self.validar_identificador(ruc):
            return {
                'success': False,
                'error': 'El RUC debe tener 11 dígitos numéricos'
            }
        
        print(f"🔍 Consultando RUC: {ruc}")
        
        # Intentar API real
        if self.token and len(self.token) > 30:
            resultado = self._consultar_api_real(ruc)
            if resultado['success']:
                return resultado
        
        # Fallback
        return self._datos_prueba(ruc)
    
    def _consultar_api_real(self, ruc: str) -> Dict[str, Any]:
        """Consulta API real"""
        try:
            url = f"{self.url_base}?numero={ruc}"
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/json"
            }
            
            response = requests.get(url, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'success': True,
                    'ruc': data.get('numeroDocumento', ruc),
                    'razon_social': data.get('razonSocial', ''),
                    'nombre_comercial': data.get('nombreComercial', ''),
                    'direccion': data.get('direccion', ''),
                    'estado': data.get('estado', ''),
                    'condicion': data.get('condicion', ''),
                    'departamento': data.get('departamento', ''),
                    'provincia': data.get('provincia', ''),
                    'distrito': data.get('distrito', ''),
                    '_fuente': 'api_real'
                }
            
            return {'success': False, 'error': f'HTTP {response.status_code}'}
            
        except Exception as e:
            return {'success': False, 'error': str(e)}