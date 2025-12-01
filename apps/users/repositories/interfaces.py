"""
Interfaces (Abstracciones) para Repositories
Siguiendo el Principio de Inversión de Dependencias (DIP)
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from django.contrib.auth.models import User


class IUsuarioRepository(ABC):
    """Interfaz para el repositorio de Usuario"""
    
    @abstractmethod
    def obtener_por_id(self, usuario_id: int):
        """Obtiene un usuario por ID"""
        pass
    
    @abstractmethod
    def obtener_por_user(self, user: User):
        """Obtiene un usuario por objeto User de Django"""
        pass
    
    @abstractmethod
    def obtener_por_email(self, email: str):
        """Obtiene un usuario por email"""
        pass
    
    @abstractmethod
    def obtener_por_dni(self, dni: str):
        """Obtiene un usuario por DNI"""
        pass
    
    @abstractmethod
    def crear(self, datos: Dict[str, Any]):
        """Crea un nuevo usuario"""
        pass
    
    @abstractmethod
    def actualizar(self, usuario, datos: Dict[str, Any]):
        """Actualiza un usuario existente"""
        pass
    
    @abstractmethod
    def listar_activos(self, tipo_usuario: Optional[str] = None) -> List:
        """Lista usuarios activos, opcionalmente filtrados por tipo"""
        pass
    
    @abstractmethod
    def buscar(self, query: str, tipo: Optional[str] = None) -> List:
        """Busca usuarios por nombre o habilidades"""
        pass


class IProfileRepository(ABC):
    """Interfaz para el repositorio de Profile"""
    
    @abstractmethod
    def obtener_por_usuario(self, usuario):
        """Obtiene el perfil de un usuario"""
        pass
    
    @abstractmethod
    def obtener_o_crear(self, usuario):
        """Obtiene o crea el perfil de un usuario"""
        pass
    
    @abstractmethod
    def actualizar(self, profile, datos: Dict[str, Any]):
        """Actualiza un perfil"""
        pass


class ICertificacionRepository(ABC):
    """Interfaz para el repositorio de Certificación"""
    
    @abstractmethod
    def listar_por_usuario(self, usuario) -> List:
        """Lista certificaciones de un usuario"""
        pass
    
    @abstractmethod
    def listar_verificadas(self, usuario) -> List:
        """Lista certificaciones verificadas de un usuario"""
        pass
    
    @abstractmethod
    def crear(self, datos: Dict[str, Any]):
        """Crea una certificación"""
        pass
    
    @abstractmethod
    def verificar(self, certificacion_id: int):
        """Marca una certificación como verificada"""
        pass


class ICalificacionRepository(ABC):
    """Interfaz para el repositorio de Calificación"""
    
    @abstractmethod
    def listar_por_receptor(self, usuario) -> List:
        """Lista calificaciones recibidas por un usuario"""
        pass
    
    @abstractmethod
    def listar_por_autor(self, usuario) -> List:
        """Lista calificaciones dadas por un usuario"""
        pass
    
    @abstractmethod
    def obtener_por_contrato(self, contrato, autor):
        """Obtiene calificación de un contrato por un autor"""
        pass
    
    @abstractmethod
    def crear(self, datos: Dict[str, Any]):
        """Crea una calificación"""
        pass
    
    @abstractmethod
    def actualizar(self, calificacion, datos: Dict[str, Any]):
        """Actualiza una calificación"""
        pass
    
    @abstractmethod
    def desactivar(self, calificacion_id: int):
        """Desactiva una calificación"""
        pass
    
    @abstractmethod
    def calcular_estadisticas(self, usuario) -> Dict[str, Any]:
        """Calcula estadísticas de calificaciones"""
        pass


class IHabilidadRepository(ABC):
    """Interfaz para el repositorio de Habilidad"""
    
    @abstractmethod
    def listar_por_usuario(self, usuario) -> List:
        """Lista habilidades de un usuario"""
        pass
    
    @abstractmethod
    def agregar_a_usuario(self, usuario, habilidad, nivel: str):
        """Agrega una habilidad a un usuario"""
        pass
    
    @abstractmethod
    def listar_activas(self) -> List:
        """Lista todas las habilidades activas"""
        pass


class ITrabajoRealizadoRepository(ABC):
    """Interfaz para el repositorio de Trabajos Realizados"""
    
    @abstractmethod
    def listar_por_usuario(self, usuario) -> List:
        """Lista trabajos realizados por un usuario"""
        pass
    
    @abstractmethod
    def crear(self, datos: Dict[str, Any]):
        """Crea un registro de trabajo realizado"""
        pass


class IVerificacionRepository(ABC):
    """Interfaz para el repositorio de Verificación"""
    
    @abstractmethod
    def obtener_por_usuario_tipo(self, usuario, tipo: str):
        """Obtiene verificación de un usuario por tipo"""
        pass
    
    @abstractmethod
    def crear(self, datos: Dict[str, Any]):
        """Crea una solicitud de verificación"""
        pass
    
    @abstractmethod
    def aprobar(self, verificacion_id: int, revisor):
        """Aprueba una verificación"""
        pass
    
    @abstractmethod
    def rechazar(self, verificacion_id: int, revisor, motivo: str):
        """Rechaza una verificación"""
        pass


class IUbicacionRepository(ABC):
    """Interfaz para el repositorio de Ubicación"""
    
    @abstractmethod
    def listar_departamentos(self) -> List:
        """Lista todos los departamentos"""
        pass
    
    @abstractmethod
    def listar_provincias(self, departamento_id: int) -> List:
        """Lista provincias de un departamento"""
        pass
    
    @abstractmethod
    def listar_distritos(self, provincia_id: int) -> List:
        """Lista distritos de una provincia"""
        pass
    
    @abstractmethod
    def listar_comunidades(self, distrito_id: int) -> List:
        """Lista comunidades de un distrito"""
        pass