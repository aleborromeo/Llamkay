"""
Servicio de Denuncias
SRP: Solo maneja lógica de negocio de denuncias
OCP: Extendible agregando nuevos tipos de denuncias
DIP: Depende de DenunciaRepository (abstracción)
"""
from typing import Optional, Dict, Any
from django.utils import timezone
import logging

from ..repositories import DenunciaRepository
from apps.users.models import Usuario
from django.contrib.auth.models import User 
from django.db.models import QuerySet

logger = logging.getLogger(__name__)


class DenunciaService:
    """
    Servicio para gestionar denuncias
    SRP: Una sola responsabilidad - lógica de denuncias
    """
    
    def __init__(self):
        self.repo = DenunciaRepository()
    
    def crear_denuncia(
        self,
        id_reportante: Usuario,
        id_denunciado: Usuario,
        motivo: str,
        descripcion: str,
        id_contrato=None,
        id_mensaje=None,
        evidencia_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Crear una nueva denuncia
        
        Args:
            id_reportante: Usuario que realiza la denuncia (instancia de Usuario)
            id_denunciado: Usuario denunciado (instancia de Usuario)
            motivo: Motivo de la denuncia
            descripcion: Descripción detallada
            id_contrato: Contrato relacionado (opcional)
            id_mensaje: Mensaje relacionado (opcional)
            evidencia_url: URL de evidencia (opcional)
        """
        try:
            # Validaciones
            if id_reportante == id_denunciado:
                return {'success': False, 'error': 'No puedes denunciarte a ti mismo'}
            
            # Verificar si ya existe una denuncia similar activa
            if self.repo.existe_denuncia_activa(id_reportante, id_denunciado, motivo):
                return {'success': False, 'error': 'Ya existe una denuncia similar en proceso'}
            
            data = {
                'id_reportante': id_reportante,
                'id_denunciado': id_denunciado,
                'motivo': motivo,
                'descripcion': descripcion,
                'id_contrato': id_contrato,
                'id_mensaje': id_mensaje,
                'evidencia_url': evidencia_url,
                'estado': 'pendiente'
            }
            
            denuncia = self.repo.create(data)
            logger.info(
                f"✅ Denuncia creada: #{denuncia.id_denuncia} - "
                f"{id_reportante.nombre_completo} vs {id_denunciado.nombre_completo}"
            )
            
            return {
                'success': True,
                'denuncia': denuncia,
                'message': 'Denuncia creada exitosamente'
            }
            
        except Exception as e:
            logger.error(f"❌ Error creando denuncia: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def actualizar_estado(
        self,
        id_denuncia: int,
        estado: str,
        id_moderador: User,
        resolucion: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Actualizar el estado de una denuncia
        
        Args:
            id_denuncia: ID de la denuncia
            estado: Nuevo estado
            id_moderador: Moderador que actualiza (instancia de User)
            resolucion: Texto de resolución (opcional)
        """
        try:
            denuncia = self.repo.get_by_id(id_denuncia)
            
            if not denuncia:
                return {'success': False, 'error': 'Denuncia no encontrada'}
            
            data = {
                'estado': estado,
                'id_moderador': id_moderador,
            }
            
            # Actualizar fechas según el estado
            if estado == 'en_revision' and not denuncia.fecha_revision:
                data['fecha_revision'] = timezone.now()
            
            if estado in ['resuelta', 'cerrada', 'rechazada']:
                data['fecha_resolucion'] = timezone.now()
                if resolucion:
                    data['resolucion'] = resolucion
            
            self.repo.update(id_denuncia, data)
            logger.info(f"✅ Denuncia #{id_denuncia} actualizada a estado: {estado}")
            
            return {'success': True, 'message': f'Denuncia actualizada a {estado}'}
            
        except Exception as e:
            logger.error(f"❌ Error actualizando denuncia: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def asignar_moderador(
        self,
        id_denuncia: int,
        id_moderador: User
    ) -> Dict[str, Any]:
        """
        Asignar un moderador a una denuncia
        
        Args:
            id_denuncia: ID de la denuncia
            id_moderador: Moderador asignado (instancia de User)
        """
        try:
            data = {
                'id_moderador': id_moderador,
                'estado': 'en_revision',
                'fecha_revision': timezone.now()
            }
            
            self.repo.update(id_denuncia, data)
            logger.info(f"✅ Moderador asignado a denuncia #{id_denuncia}")
            
            return {'success': True, 'message': 'Moderador asignado exitosamente'}
            
        except Exception as e:
            logger.error(f"❌ Error asignando moderador: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def resolver_denuncia(
        self,
        id_denuncia: int,
        resolucion: str,
        id_moderador: User
    ) -> Dict[str, Any]:
        """Resolver una denuncia"""
        return self.actualizar_estado(
            id_denuncia=id_denuncia,
            estado='resuelta',
            id_moderador=id_moderador,
            resolucion=resolucion
        )
    
    def rechazar_denuncia(
        self,
        id_denuncia: int,
        motivo_rechazo: str,
        id_moderador: User
    ) -> Dict[str, Any]:
        """Rechazar una denuncia"""
        return self.actualizar_estado(
            id_denuncia=id_denuncia,
            estado='rechazada',
            id_moderador=id_moderador,
            resolucion=motivo_rechazo
        )
    
    def cerrar_denuncia(
        self,
        id_denuncia: int,
        id_moderador: User
    ) -> Dict[str, Any]:
        """Cerrar una denuncia"""
        return self.actualizar_estado(
            id_denuncia=id_denuncia,
            estado='cerrada',
            id_moderador=id_moderador
        )
    
    # ==================== CONSULTAS ====================
    
    def obtener_denuncias_usuario(self, usuario: Usuario) -> QuerySet:
        """
        Obtiene denuncias del usuario reportante
        :param usuario: instancia de apps.users.models.Usuario
        """
        if not isinstance(usuario, Usuario):
            raise ValueError("Debe ser una instancia de Usuario")
        
        return self.repo.get_by_reportante(usuario)
    
    def obtener_denuncias_recibidas(self, usuario: Usuario) -> QuerySet:
        """
        Obtener denuncias recibidas por un usuario
        :param usuario: instancia de apps.users.models.Usuario
        """
        if not isinstance(usuario, Usuario):
            raise ValueError("Debe ser una instancia de Usuario")
        
        return self.repo.get_by_denunciado(usuario)
    
    def obtener_denuncias_por_estado(self, estado: str) -> QuerySet:
        """
        Obtener denuncias por estado
        :param estado: Estado de la denuncia (pendiente, en_revision, etc.)
        """
        return self.repo.get_by_estado(estado)
    
    def obtener_denuncias_moderador(self, moderador: User) -> QuerySet:
        """
        Obtener denuncias moderadas por un usuario
        :param moderador: instancia de django.contrib.auth.models.User
        """
        return self.repo.get_by_moderador(moderador)
    
    def obtener_todas_denuncias(self) -> QuerySet:
        """Obtener todas las denuncias"""
        return self.repo.get_all()
    
    def contar_denuncias_usuario(self, usuario: Usuario) -> int:
        """
        Contar denuncias recibidas por un usuario
        :param usuario: instancia de apps.users.models.Usuario
        """
        if not isinstance(usuario, Usuario):
            raise ValueError("Debe ser una instancia de Usuario")
        
        return self.repo.count_by_denunciado(usuario)
    
    def obtener_estadisticas_usuario(self, usuario: Usuario) -> Dict[str, int]:
        """
        Obtener estadísticas de denuncias de un usuario
        :param usuario: instancia de apps.users.models.Usuario
        """
        if not isinstance(usuario, Usuario):
            raise ValueError("Debe ser una instancia de Usuario")
        
        return {
            'total': self.repo.count_by_denunciado(usuario),
            'pendientes': self.repo.count_by_estado_and_denunciado(usuario, 'pendiente'),
            'en_revision': self.repo.count_by_estado_and_denunciado(usuario, 'en_revision'),
            'resueltas': self.repo.count_by_estado_and_denunciado(usuario, 'resuelta'),
            'rechazadas': self.repo.count_by_estado_and_denunciado(usuario, 'rechazada'),
        }