"""
Consultor de API RENIEC (DNI)
Usa apis.net.pe/v1 con token Bearer
"""

import requests
from typing import Dict, Any

from .base import ConsultorAPIBase


class ConsultorRENIEC(ConsultorAPIBase):
    """
    Consultor para verificación de DNI usando API v1
    """
    
    def __init__(self, token: str = None):
        super().__init__(token or "")
        self.url_base = "https://api.apis.net.pe/v1/dni"
    
    def validar_identificador(self, dni: str) -> bool:
        """Valida que el DNI tenga formato correcto"""
        if not dni:
            return False
        return len(dni) == 8 and dni.isdigit()
    
    def consultar(self, dni: str) -> Dict[str, Any]:
        """
        Consulta información de un DNI
        
        Args:
            dni: Número de DNI a consultar
            
        Returns:
            Dict con la información del ciudadano
        """
        # Validar formato
        if not self.validar_identificador(dni):
            return {
                'success': False,
                'error': 'El DNI debe tener 8 dígitos numéricos'
            }
        
        print(f"🔍 Consultando DNI: {dni}")
        
        # Verificar que hay token
        if not self.token:
            return {
                'success': False,
                'error': 'Token de API no configurado'
            }
        
        return self._consultar_api_real(dni)
    
    def _consultar_api_real(self, dni: str) -> Dict[str, Any]:
        """
        Consulta la API real de apis.net.pe v1
        
        Args:
            dni: DNI a consultar
            
        Returns:
            Dict con resultado de la consulta
        """
        try:
            url = f"{self.url_base}?numero={dni}"
            
            # 🔑 Headers con Bearer Token
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/json"
            }
            
            print(f"📡 URL: {url}")
            print(f"📡 Headers: Authorization: Bearer {self.token[:30]}...")
            
            response = requests.get(
                url,
                headers=headers,
                timeout=self.timeout
            )
            
            print(f"📡 Status Code: {response.status_code}")
            
            # ✅ Respuesta exitosa
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Datos recibidos: {data}")
                
                # Construir nombre completo
                nombres = data.get('nombres', '')
                apellido_paterno = data.get('apellidoPaterno', '')
                apellido_materno = data.get('apellidoMaterno', '')
                nombre_completo = f"{nombres} {apellido_paterno} {apellido_materno}".strip()
                
                return {
                    'success': True,
                    'dni': dni,
                    'nombres': nombres,
                    'apellido_paterno': apellido_paterno,
                    'apellido_materno': apellido_materno,
                    'nombre_completo': nombre_completo,
                    '_fuente': 'api_real'
                }
            
            # ❌ Errores HTTP
            elif response.status_code == 401:
                print("❌ Token inválido o expirado")
                return {
                    'success': False,
                    'error': 'Token inválido o expirado'
                }
            
            elif response.status_code == 404:
                print("❌ DNI no encontrado")
                return {
                    'success': False,
                    'error': 'No se encontró el DNI'
                }
            
            else:
                error_text = response.text[:200]
                print(f"❌ Error HTTP {response.status_code}: {error_text}")
                return {
                    'success': False,
                    'error': f'Error al consultar el DNI (HTTP {response.status_code})'
                }
            
        except requests.exceptions.Timeout:
            print("❌ Timeout")
            return {
                'success': False,
                'error': 'Tiempo de espera agotado'
            }
            
        except requests.exceptions.ConnectionError:
            print("❌ Error de conexión")
            return {
                'success': False,
                'error': 'Error de conexión con el servicio'
            }
            
        except Exception as e:
            print(f"❌ Error inesperado: {str(e)}")
            return {
                'success': False,
                'error': f'Error al consultar el DNI: {str(e)}'
            }