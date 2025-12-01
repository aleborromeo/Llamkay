"""
Servicio de Calificaciones
Responsabilidad: Lógica de negocio para calificaciones
"""

from typing import Dict, Any, Optional, List
from django.db.models import Q

from apps.users.models import Usuario
from apps.users.repositories import CalificacionRepository
from apps.jobs.models import Contrato, Calificacion
from .estadistica_service import EstadisticaService


class CalificacionService:
    """
    Servicio para gestionar calificaciones
    """
    
    def __init__(
        self,
        calificacion_repo: Optional[CalificacionRepository] = None,
        estadistica_service: Optional[EstadisticaService] = None
    ):
        self.calificacion_repo = calificacion_repo or CalificacionRepository()
        self.estadistica_service = estadistica_service or EstadisticaService()
    
    def crear_calificacion(
        self,
        autor: Usuario,
        receptor: Usuario,
        contrato: Contrato,
        datos: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Crea una nueva calificación
        Valida que exista un contrato completado
        """
        # Validar que no sea el mismo usuario
        if autor.id_usuario == receptor.id_usuario:
            return {
                'success': False,
                'error': 'No puedes calificarte a ti mismo'
            }
        
        # Validar que existe un contrato completado
        contrato_valido = Contrato.objects.filter(
            Q(id_empleador=autor, id_trabajador=receptor) |
            Q(id_empleador=receptor, id_trabajador=autor),
            estado='completado'
        ).first()
        
        if not contrato_valido:
            return {
                'success': False,
                'error': 'No tienes un contrato completado con este usuario'
            }
        
        # Determinar rol del autor
        if contrato_valido.id_empleador.id_usuario == autor.id_usuario:
            rol_autor = 'empleador'
        else:
            rol_autor = 'trabajador'
        
        # Verificar si ya existe calificación
        calificacion_existente = self.calificacion_repo.obtener_por_contrato(
            contrato_valido,
            autor
        )
        
        if calificacion_existente:
            # Actualizar calificación existente
            self.calificacion_repo.actualizar(calificacion_existente, datos)
            mensaje = 'Calificación actualizada correctamente'
        else:
            # Crear nueva calificación
            datos_completos = {
                'id_contrato': contrato_valido,
                'id_autor': autor,
                'id_receptor': receptor,
                'rol_autor': rol_autor,
                **datos
            }
            self.calificacion_repo.crear(datos_completos)
            mensaje = 'Calificación creada correctamente'
        
        # Actualizar estadísticas
        self.estadistica_service.actualizar_calificaciones(receptor)
        
        return {
            'success': True,
            'message': mensaje
        }
    
    def obtener_calificaciones_usuario(
        self,
        usuario_id: int
    ) -> Dict[str, Any]:
        """
        Obtiene todas las calificaciones de un usuario con estadísticas
        """
        from apps.users.repositories import UsuarioRepository
        usuario_repo = UsuarioRepository()
        
        usuario = usuario_repo.obtener_por_id(usuario_id)
        if not usuario:
            return {
                'success': False,
                'error': 'Usuario no encontrado'
            }
        
        # Obtener calificaciones
        calificaciones = self.calificacion_repo.listar_por_receptor(usuario)
        
        # Calcular estadísticas
        estadisticas = self.calificacion_repo.calcular_estadisticas(usuario)
        
        return {
            'success': True,
            'usuario': usuario,
            'calificaciones': calificaciones,
            **estadisticas
        }
    
    def eliminar_calificacion(
        self,
        calificacion_id: int,
        autor: Usuario
    ) -> Dict[str, Any]:
        """
        Elimina (desactiva) una calificación
        Solo el autor puede eliminarla
        """
        try:
            calificacion = Calificacion.objects.get(
                id_calificacion=calificacion_id,
                id_autor=autor
            )
            
            receptor = calificacion.id_receptor
            
            # Desactivar
            self.calificacion_repo.desactivar(calificacion_id)
            
            # Actualizar estadísticas
            self.estadistica_service.actualizar_calificaciones(receptor)
            
            return {
                'success': True,
                'message': 'Calificación eliminada correctamente'
            }
            
        except Calificacion.DoesNotExist:
            return {
                'success': False,
                'error': 'Calificación no encontrada o no tienes permisos'
            }
    
    def obtener_mis_calificaciones(
        self,
        usuario: Usuario
    ) -> Dict[str, Any]:
        """
        Obtiene calificaciones dadas y recibidas por el usuario
        """
        recibidas = self.calificacion_repo.listar_por_receptor(usuario)
        dadas = self.calificacion_repo.listar_por_autor(usuario)
        
        return {
            'success': True,
            'calificaciones_recibidas': recibidas,
            'calificaciones_dadas': dadas,
            'usuario': usuario,
        }