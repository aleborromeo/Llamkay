"""
Repositorio para Postulaciones
Responsabilidad: Acceso a datos de postulaciones
"""
from typing import Optional
from django.db.models import Q, QuerySet
from apps.jobs.models import Postulacion


class PostulacionRepository:
    """
    Repositorio para gestionar acceso a datos de postulaciones
    Principio de Responsabilidad Única (SOLID)
    """
    
    @staticmethod
    def get_by_id(postulacion_id: int) -> Optional[Postulacion]:
        """Obtiene una postulación por ID"""
        try:
            return Postulacion.objects.select_related(
                'id_trabajador',
                'id_oferta_usuario',
                'id_oferta_empresa'
            ).get(id_postulacion=postulacion_id)
        except Postulacion.DoesNotExist:
            return None
    
    @staticmethod
    def existe_postulacion(trabajador_id: int, oferta_id: int, tipo_oferta: str) -> bool:
        """
        Verifica si ya existe una postulación
        
        Args:
            trabajador_id: ID del trabajador
            oferta_id: ID de la oferta
            tipo_oferta: 'usuario' o 'empresa'
        """
        filtro = {'id_trabajador_id': trabajador_id}
        
        if tipo_oferta == 'usuario':
            filtro['id_oferta_usuario_id'] = oferta_id
        else:
            filtro['id_oferta_empresa_id'] = oferta_id
        
        return Postulacion.objects.filter(**filtro).exists()
    
    @staticmethod
    def get_postulaciones_trabajador(
        trabajador_id: int,
        estado: Optional[str] = None
    ) -> QuerySet:
        """
        Obtiene todas las postulaciones de un trabajador
        
        Args:
            trabajador_id: ID del trabajador
            estado: Filtro opcional por estado
        """
        queryset = Postulacion.objects.filter(
            id_trabajador_id=trabajador_id
        ).select_related(
            'id_oferta_usuario',
            'id_oferta_usuario__id_empleador',
            'id_oferta_usuario__id_categoria',
            'id_oferta_empresa',
            'id_oferta_empresa__id_empleador',
            'id_oferta_empresa__id_categoria',
        ).order_by('-created_at')
        
        if estado:
            queryset = queryset.filter(estado=estado)
        
        return queryset
    
    @staticmethod
    def get_postulaciones_empleador(
        empleador_id: int,
        estado: Optional[str] = None
    ) -> QuerySet:
        """
        Obtiene todas las postulaciones recibidas por un empleador
        
        Args:
            empleador_id: ID del empleador
            estado: Filtro opcional por estado
        """
        queryset = Postulacion.objects.filter(
            Q(id_oferta_usuario__id_empleador_id=empleador_id) |
            Q(id_oferta_empresa__id_empleador_id=empleador_id)
        ).select_related(
            'id_trabajador',
            'id_oferta_usuario',
            'id_oferta_empresa',
        ).order_by('-created_at')
        
        if estado:
            queryset = queryset.filter(estado=estado)
        
        return queryset
    
    @staticmethod
    def get_postulaciones_oferta(oferta_id: int, tipo_oferta: str) -> QuerySet:
        """
        Obtiene todas las postulaciones de una oferta específica
        
        Args:
            oferta_id: ID de la oferta
            tipo_oferta: 'usuario' o 'empresa'
        """
        if tipo_oferta == 'usuario':
            return Postulacion.objects.filter(
                id_oferta_usuario_id=oferta_id
            ).select_related('id_trabajador').order_by('-created_at')
        else:
            return Postulacion.objects.filter(
                id_oferta_empresa_id=oferta_id
            ).select_related('id_trabajador').order_by('-created_at')
    
    @staticmethod
    def crear_postulacion(data: dict) -> Postulacion:
        """
        Crea una nueva postulación
        
        Args:
            data: Dict con datos de la postulación
        """
        return Postulacion.objects.create(**data)
    
    @staticmethod
    def actualizar_estado(postulacion_id: int, nuevo_estado: str) -> bool:
        """
        Actualiza el estado de una postulación
        
        Args:
            postulacion_id: ID de la postulación
            nuevo_estado: Nuevo estado
        """
        try:
            postulacion = Postulacion.objects.get(id_postulacion=postulacion_id)
            postulacion.estado = nuevo_estado
            postulacion.save(update_fields=['estado', 'updated_at'])
            return True
        except Postulacion.DoesNotExist:
            return False
    
    @staticmethod
    def eliminar_postulacion(postulacion_id: int) -> bool:
        """Elimina una postulación"""
        try:
            postulacion = Postulacion.objects.get(id_postulacion=postulacion_id)
            postulacion.delete()
            return True
        except Postulacion.DoesNotExist:
            return False
    
    @staticmethod
    def contar_postulaciones_trabajador(trabajador_id: int) -> dict:
        """
        Cuenta postulaciones por estado de un trabajador
        
        Returns:
            Dict con contadores por estado
        """
        postulaciones = Postulacion.objects.filter(id_trabajador_id=trabajador_id)
        
        return {
            'total': postulaciones.count(),
            'pendientes': postulaciones.filter(estado='pendiente').count(),
            'aceptadas': postulaciones.filter(estado='aceptada').count(),
            'rechazadas': postulaciones.filter(estado='rechazada').count(),
        }
    
    @staticmethod
    def contar_postulaciones_empleador(empleador_id: int) -> dict:
        """
        Cuenta postulaciones recibidas por un empleador
        
        Returns:
            Dict con contadores
        """
        postulaciones = Postulacion.objects.filter(
            Q(id_oferta_usuario__id_empleador_id=empleador_id) |
            Q(id_oferta_empresa__id_empleador_id=empleador_id)
        )
        
        return {
            'total': postulaciones.count(),
            'pendientes': postulaciones.filter(estado='pendiente').count(),
            'aceptadas': postulaciones.filter(estado='aceptada').count(),
            'rechazadas': postulaciones.filter(estado='rechazada').count(),
        }