"""
Repositorio de Ofertas para Empleadores
Responsabilidad: Acceso a datos de ofertas desde perspectiva del empleador
"""
from typing import Optional, List
from django.db.models import Q, Count, QuerySet
from apps.jobs.models import OfertaUsuario, OfertaEmpresa


class OfertaEmpleadorRepository:
    """
    Repositorio para gestionar ofertas desde el lado del empleador
    Principio de Responsabilidad Única (SOLID)
    """
    
    @staticmethod
    def get_ofertas_empleador_usuario(empleador_id: int, estado: Optional[str] = None) -> QuerySet:
        """
        Obtiene ofertas individuales de un empleador
        
        Args:
            empleador_id: ID del empleador
            estado: Filtro opcional por estado
        """
        queryset = OfertaUsuario.objects.filter(
            id_empleador_id=empleador_id
        ).select_related(
            'id_categoria',
            'id_departamento',
            'id_provincia',
            'id_distrito'
        ).annotate(
            total_postulaciones_count=Count('postulaciones'),
            postulaciones_pendientes_count=Count(
                'postulaciones',
                filter=Q(postulaciones__estado='pendiente')
            )
        ).order_by('-created_at')
        
        if estado:
            queryset = queryset.filter(estado=estado)
        
        return queryset
    
    @staticmethod
    def get_ofertas_empleador_empresa(empleador_id: int, estado: Optional[str] = None) -> QuerySet:
        """
        Obtiene ofertas de empresa de un empleador
        
        Args:
            empleador_id: ID del empleador
            estado: Filtro opcional por estado
        """
        queryset = OfertaEmpresa.objects.filter(
            id_empleador_id=empleador_id
        ).select_related(
            'id_categoria',
            'id_departamento',
            'id_provincia',
            'id_distrito'
        ).annotate(
            total_postulaciones_count=Count('postulaciones'),
            postulaciones_pendientes_count=Count(
                'postulaciones',
                filter=Q(postulaciones__estado='pendiente')
            )
        ).order_by('-created_at')
        
        if estado:
            queryset = queryset.filter(estado=estado)
        
        return queryset
    
    @staticmethod
    def get_oferta_usuario_by_id_empleador(oferta_id: int, empleador_id: int) -> Optional[OfertaUsuario]:
        """
        Obtiene una oferta individual validando que pertenece al empleador
        
        Args:
            oferta_id: ID de la oferta
            empleador_id: ID del empleador
        """
        try:
            return OfertaUsuario.objects.get(
                id=oferta_id,
                id_empleador_id=empleador_id
            )
        except OfertaUsuario.DoesNotExist:
            return None
    
    @staticmethod
    def get_oferta_empresa_by_id_empleador(oferta_id: int, empleador_id: int) -> Optional[OfertaEmpresa]:
        """
        Obtiene una oferta de empresa validando que pertenece al empleador
        
        Args:
            oferta_id: ID de la oferta
            empleador_id: ID del empleador
        """
        try:
            return OfertaEmpresa.objects.get(
                id=oferta_id,
                id_empleador_id=empleador_id
            )
        except OfertaEmpresa.DoesNotExist:
            return None
    
    @staticmethod
    def crear_oferta_usuario(data: dict) -> OfertaUsuario:
        """
        Crea una oferta individual
        
        Args:
            data: Dict con datos de la oferta
        """
        return OfertaUsuario.objects.create(**data)
    
    @staticmethod
    def crear_oferta_empresa(data: dict) -> OfertaEmpresa:
        """
        Crea una oferta de empresa
        
        Args:
            data: Dict con datos de la oferta
        """
        return OfertaEmpresa.objects.create(**data)
    
    @staticmethod
    def actualizar_oferta_usuario(oferta_id: int, empleador_id: int, data: dict) -> bool:
        """
        Actualiza una oferta individual
        
        Args:
            oferta_id: ID de la oferta
            empleador_id: ID del empleador (validación)
            data: Dict con datos a actualizar
        """
        try:
            oferta = OfertaUsuario.objects.get(
                id=oferta_id,
                id_empleador_id=empleador_id
            )
            for key, value in data.items():
                setattr(oferta, key, value)
            oferta.save()
            return True
        except OfertaUsuario.DoesNotExist:
            return False
    
    @staticmethod
    def actualizar_oferta_empresa(oferta_id: int, empleador_id: int, data: dict) -> bool:
        """
        Actualiza una oferta de empresa
        
        Args:
            oferta_id: ID de la oferta
            empleador_id: ID del empleador (validación)
            data: Dict con datos a actualizar
        """
        try:
            oferta = OfertaEmpresa.objects.get(
                id=oferta_id,
                id_empleador_id=empleador_id
            )
            for key, value in data.items():
                setattr(oferta, key, value)
            oferta.save()
            return True
        except OfertaEmpresa.DoesNotExist:
            return False
    
    @staticmethod
    def cambiar_estado_oferta(oferta_id: int, empleador_id: int, nuevo_estado: str, tipo: str) -> bool:
        """
        Cambia el estado de una oferta
        
        Args:
            oferta_id: ID de la oferta
            empleador_id: ID del empleador (validación)
            nuevo_estado: Nuevo estado
            tipo: 'usuario' o 'empresa'
        """
        try:
            if tipo == 'usuario':
                oferta = OfertaUsuario.objects.get(
                    id=oferta_id,
                    id_empleador_id=empleador_id
                )
            else:
                oferta = OfertaEmpresa.objects.get(
                    id=oferta_id,
                    id_empleador_id=empleador_id
                )
            
            oferta.estado = nuevo_estado
            oferta.save(update_fields=['estado', 'updated_at'])
            return True
        except (OfertaUsuario.DoesNotExist, OfertaEmpresa.DoesNotExist):
            return False
    
    @staticmethod
    def contar_ofertas_empleador(empleador_id: int) -> dict:
        """
        Cuenta las ofertas de un empleador por tipo y estado
        
        Returns:
            Dict con contadores
        """
        ofertas_usuario = OfertaUsuario.objects.filter(id_empleador_id=empleador_id)
        ofertas_empresa = OfertaEmpresa.objects.filter(id_empleador_id=empleador_id)
        
        return {
            'total_ofertas_usuario': ofertas_usuario.count(),
            'total_ofertas_empresa': ofertas_empresa.count(),
            'ofertas_activas': (
                ofertas_usuario.filter(estado='activa').count() +
                ofertas_empresa.filter(estado='activa').count()
            ),
            'ofertas_pausadas': (
                ofertas_usuario.filter(estado='pausada').count() +
                ofertas_empresa.filter(estado='pausada').count()
            ),
            'ofertas_cerradas': (
                ofertas_usuario.filter(estado='cerrada').count() +
                ofertas_empresa.filter(estado='cerrada').count()
            ),
        }
    
    @staticmethod
    def get_ofertas_activas_recientes(empleador_id: int, limit: int = 5) -> List:
        """
        Obtiene las ofertas activas más recientes
        
        Args:
            empleador_id: ID del empleador
            limit: Límite de resultados
        """
        ofertas_usuario = OfertaUsuario.objects.filter(
            id_empleador_id=empleador_id,
            estado='activa'
        ).select_related('id_categoria').annotate(
            postulaciones_count=Count('postulaciones')
        ).order_by('-created_at')[:limit]
        
        ofertas_empresa = OfertaEmpresa.objects.filter(
            id_empleador_id=empleador_id,
            estado='activa'
        ).select_related('id_categoria').annotate(
            postulaciones_count=Count('postulaciones')
        ).order_by('-created_at')[:limit]
        
        # Combinar y ordenar
        todas_ofertas = []
        
        for oferta in ofertas_usuario:
            todas_ofertas.append({
                'tipo': 'usuario',
                'id': oferta.id,
                'titulo': oferta.titulo,
                'estado': oferta.estado,
                'vistas': oferta.vistas,
                'postulaciones': oferta.postulaciones_count,
                'fecha': oferta.created_at,
            })
        
        for oferta in ofertas_empresa:
            todas_ofertas.append({
                'tipo': 'empresa',
                'id': oferta.id,
                'titulo': oferta.titulo_puesto,
                'estado': oferta.estado,
                'vistas': oferta.vistas,
                'postulaciones': oferta.postulaciones_count,
                'fecha': oferta.created_at,
            })
        
        # Ordenar por fecha
        todas_ofertas.sort(key=lambda x: x['fecha'], reverse=True)
        
        return todas_ofertas[:limit]