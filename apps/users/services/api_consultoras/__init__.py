"""
API Consultoras
Servicios para consulta de APIs externas siguiendo OCP
"""

from django.conf import settings
from typing import Dict, Any
import sys

from .base import ConsultorAPIBase
from .reniec_consultor import ConsultorRENIEC
from .sunat_consultor import ConsultorSUNAT


class APIService:
    """
    Servicio coordinador de todas las APIs
    Implementa el patrón Strategy
    """
    
    def __init__(self, token: str = None):
        """
        Inicializa el servicio con el token de API
        
        Args:
            token: Token de autenticación (usa settings si no se provee)
        """
        # ✅ INTENTAR OBTENER TOKEN DE VARIAS FORMAS
        if token:
            self.token = token
        elif hasattr(settings, 'APIPERU_TOKEN'):
            self.token = settings.APIPERU_TOKEN
        else:
            # Buscar en el módulo de settings directamente
            try:
                import config.settings.base as base_settings
                self.token = base_settings.APIPERU_TOKEN
                print("⚠️ Token obtenido directamente de base.py")
            except:
                self.token = ''
                print("❌ No se pudo obtener el token de ninguna fuente")
        
        # ✅ DEBUG: Verificar que el token se cargó
        print(f"\n{'='*60}")
        print("🏗️ APIService.__init__")
        print(f"{'='*60}")
        print(f"🔑 Token recibido como parámetro: {'SÍ' if token else 'NO'}")
        print(f"🔑 Token en settings: {'SÍ' if hasattr(settings, 'APIPERU_TOKEN') else 'NO'}")
        print(f"🔑 Token final cargado: {'SÍ' if self.token else 'NO'}")
        if self.token:
            print(f"🔑 Token valor: {self.token[:20]}...")
        print(f"{'='*60}\n")
        
        # Registrar consultores disponibles
        self.consultores = {
            'dni': ConsultorRENIEC(self.token),
            'ruc': ConsultorSUNAT(self.token),
        }
        
        print(f"✅ Consultores registrados: {list(self.consultores.keys())}\n")
    
    def consultar(self, tipo: str, identificador: str) -> Dict[str, Any]:
        """
        Consulta cualquier API registrada
        
        Args:
            tipo: Tipo de consulta ('dni', 'ruc')
            identificador: Identificador a consultar
            
        Returns:
            Dict con el resultado de la consulta
        """
        print(f"📞 APIService.consultar llamado - Tipo: {tipo}, ID: {identificador}")
        
        consultor = self.consultores.get(tipo)
        
        if not consultor:
            print(f"❌ Consultor '{tipo}' no encontrado")
            return {
                'success': False,
                'error': f"Tipo de consulta '{tipo}' no soportada"
            }
        
        print(f"✅ Consultor encontrado: {consultor.__class__.__name__}")
        resultado = consultor.consultar(identificador)
        print(f"📦 Resultado: {resultado}\n")
        
        return resultado
    
    def registrar_consultor(self, tipo: str, consultor: ConsultorAPIBase) -> None:
        """
        Registra un nuevo consultor dinámicamente
        Permite extender sin modificar (OCP)
        
        Args:
            tipo: Tipo de identificador
            consultor: Instancia del consultor
        """
        self.consultores[tipo] = consultor
    
    def tipos_disponibles(self) -> list:
        """
        Retorna los tipos de consulta disponibles
        
        Returns:
            Lista de tipos registrados
        """
        return list(self.consultores.keys())


__all__ = [
    'ConsultorAPIBase',
    'ConsultorRENIEC',
    'ConsultorSUNAT',
    'APIService',
]