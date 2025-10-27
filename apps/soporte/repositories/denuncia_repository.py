"""
Repositorio para Denuncias
SRP: Solo maneja acceso a datos de Denuncias
DIP: Implementa abstracción para acceso a datos
"""
from typing import Optional, List
from django.db.models import Q, QuerySet
from ..models import Denuncia


class DenunciaRepository:
    """
    Capa de acceso a datos para Denuncias
    SRP: Una sola responsabilidad - acceso a datos
    """
    
    @staticmethod
    def create(data: dict) -> Denuncia:
        """Crear nueva denuncia"""
        return Denuncia.objects.create(**data)
    
    @staticmethod
    def get_by_id(id_denuncia: int) -> Optional[Denuncia]:
        """Obtener denuncia por ID"""
        try:
            return Denuncia.objects.select_related(
                'id_reportante',
                'id_denunciado',
                'id_moderador',
                'id_contrato',
                'id_mensaje'
            ).get(id_denuncia=id_denuncia)
        except Denuncia.DoesNotExist:
            return None
    
    @staticmethod
    def get_by_reportante(id_reportante) -> QuerySet:
        """Obtener denuncias realizadas por un usuario"""
        return Denuncia.objects.filter(
            id_reportante=id_reportante
        ).select_related(
            'id_denunciado',
            'id_moderador'
        ).order_by('-fecha')
    
    @staticmethod
    def get_by_denunciado(id_denunciado) -> QuerySet:
        """Obtener denuncias recibidas por un usuario"""
        return Denuncia.objects.filter(
            id_denunciado=id_denunciado
        ).select_related(
            'id_reportante',
            'id_moderador'
        ).order_by('-fecha')
    
    @staticmethod
    def get_by_estado(estado: str) -> QuerySet:
        """Obtener denuncias por estado"""
        return Denuncia.objects.filter(
            estado=estado
        ).select_related(
            'id_reportante',
            'id_denunciado',
            'id_moderador'
        ).order_by('-fecha')
    
    @staticmethod
    def get_by_moderador(id_moderador) -> QuerySet:
        """Obtener denuncias moderadas por un usuario"""
        return Denuncia.objects.filter(
            id_moderador=id_moderador
        ).select_related(
            'id_reportante',
            'id_denunciado'
        ).order_by('-fecha_revision')
    
    @staticmethod
    def get_all() -> QuerySet:
        """Obtener todas las denuncias"""
        return Denuncia.objects.select_related(
            'id_reportante',
            'id_denunciado',
            'id_moderador'
        ).order_by('-fecha')
    
    @staticmethod
    def update(id_denuncia: int, data: dict) -> bool:
        """Actualizar denuncia"""
        updated = Denuncia.objects.filter(
            id_denuncia=id_denuncia
        ).update(**data)
        return updated > 0
    
    @staticmethod
    def count_by_denunciado(id_denunciado) -> int:
        """Contar denuncias de un usuario"""
        return Denuncia.objects.filter(
            id_denunciado=id_denunciado
        ).count()
    
    @staticmethod
    def count_by_estado_and_denunciado(id_denunciado, estado: str) -> int:
        """Contar denuncias por estado de un usuario"""
        return Denuncia.objects.filter(
            id_denunciado=id_denunciado,
            estado=estado
        ).count()
    
    @staticmethod
    def existe_denuncia_activa(id_reportante, id_denunciado, motivo: str) -> bool:
        """Verificar si ya existe una denuncia activa similar"""
        return Denuncia.objects.filter(
            id_reportante=id_reportante,
            id_denunciado=id_denunciado,
            motivo=motivo,
            estado__in=['pendiente', 'en_revision']
        ).exists()