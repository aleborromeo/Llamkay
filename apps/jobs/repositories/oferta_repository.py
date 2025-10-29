"""
Repositorio para Ofertas
Responsabilidad: Acceso a datos de ofertas (queries)
"""
from typing import Optional, List
from django.db.models import Q, Count, QuerySet
from apps.jobs.models import OfertaUsuario, OfertaEmpresa


class OfertaRepository:
    """
    Repositorio para gestionar acceso a datos de ofertas
    Principio de Responsabilidad Única (SOLID)
    """
    
    @staticmethod
    def get_oferta_usuario_by_id(oferta_id: int) -> Optional[OfertaUsuario]:
        """Obtiene una oferta de usuario por ID"""
        try:
            return OfertaUsuario.objects.select_related(
                'id_empleador',
                'id_categoria',
                'id_departamento',
                'id_provincia',
                'id_distrito'
            ).get(id=oferta_id)
        except OfertaUsuario.DoesNotExist:
            return None
    
    @staticmethod
    def get_oferta_empresa_by_id(oferta_id: int) -> Optional[OfertaEmpresa]:
        """Obtiene una oferta de empresa por ID"""
        try:
            return OfertaEmpresa.objects.select_related(
                'id_empleador',
                'id_categoria',
                'id_departamento',
                'id_provincia',
                'id_distrito'
            ).get(id=oferta_id)
        except OfertaEmpresa.DoesNotExist:
            return None
    
    @staticmethod
    def get_ofertas_activas_usuario(limit: Optional[int] = None) -> QuerySet:
        """Obtiene ofertas activas de usuarios"""
        queryset = OfertaUsuario.objects.select_related(
            'id_empleador',
            'id_categoria',
            'id_departamento',
            'id_provincia',
            'id_distrito'
        ).filter(estado='activa').order_by('-created_at')
        
        if limit:
            queryset = queryset[:limit]
        
        return queryset
    
    @staticmethod
    def get_ofertas_activas_empresa(limit: Optional[int] = None) -> QuerySet:
        """Obtiene ofertas activas de empresas"""
        queryset = OfertaEmpresa.objects.select_related(
            'id_empleador',
            'id_categoria',
            'id_departamento',
            'id_provincia',
            'id_distrito'
        ).filter(estado='activa').order_by('-created_at')
        
        if limit:
            queryset = queryset[:limit]
        
        return queryset
    
    @staticmethod
    def buscar_ofertas_usuario(filtros: dict, excluir_empleador=None) -> QuerySet:
        """
        Busca ofertas de usuario con filtros
        
        Args:
            filtros: Dict con claves: busqueda, departamento, provincia, distrito, categoria
            excluir_empleador: Usuario a excluir (para no mostrar sus propias ofertas)
        """
        queryset = OfertaUsuario.objects.select_related(
            'id_empleador',
            'id_categoria',
            'id_departamento',
            'id_provincia',
            'id_distrito'
        ).filter(estado='activa')
        
        if excluir_empleador:
            queryset = queryset.exclude(id_empleador=excluir_empleador)
        
        if filtros.get('busqueda'):
            busqueda = filtros['busqueda']
            queryset = queryset.filter(
                Q(titulo__icontains=busqueda) |
                Q(descripcion__icontains=busqueda) |
                Q(id_categoria__nombre__icontains=busqueda)
            )
        
        if filtros.get('departamento'):
            queryset = queryset.filter(id_departamento=filtros['departamento'])
        
        if filtros.get('provincia'):
            queryset = queryset.filter(id_provincia=filtros['provincia'])
        
        if filtros.get('distrito'):
            queryset = queryset.filter(id_distrito=filtros['distrito'])
        
        if filtros.get('categoria'):
            queryset = queryset.filter(id_categoria=filtros['categoria'])
        
        return queryset.annotate(
            postulaciones_count=Count('postulaciones', filter=Q(postulaciones__estado='pendiente'))
        ).order_by('-created_at')
    
    @staticmethod
    def buscar_ofertas_empresa(filtros: dict, excluir_empleador=None) -> QuerySet:
        """
        Busca ofertas de empresa con filtros
        
        Args:
            filtros: Dict con claves: busqueda, departamento, provincia, distrito, categoria
            excluir_empleador: Usuario a excluir
        """
        queryset = OfertaEmpresa.objects.select_related(
            'id_empleador',
            'id_categoria',
            'id_departamento',
            'id_provincia',
            'id_distrito'
        ).filter(estado='activa')
        
        if excluir_empleador:
            queryset = queryset.exclude(id_empleador=excluir_empleador)
        
        if filtros.get('busqueda'):
            busqueda = filtros['busqueda']
            queryset = queryset.filter(
                Q(titulo_puesto__icontains=busqueda) |
                Q(descripcion__icontains=busqueda) |
                Q(id_categoria__nombre__icontains=busqueda)
            )
        
        if filtros.get('departamento'):
            queryset = queryset.filter(id_departamento=filtros['departamento'])
        
        if filtros.get('provincia'):
            queryset = queryset.filter(id_provincia=filtros['provincia'])
        
        if filtros.get('distrito'):
            queryset = queryset.filter(id_distrito=filtros['distrito'])
        
        if filtros.get('categoria'):
            queryset = queryset.filter(id_categoria=filtros['categoria'])
        
        return queryset.annotate(
            postulaciones_count=Count('postulaciones', filter=Q(postulaciones__estado='pendiente'))
        ).order_by('-created_at')
    
    @staticmethod
    def incrementar_vistas(oferta_id: int, tipo: str) -> bool:
        """Incrementa el contador de vistas de una oferta"""
        try:
            if tipo == 'usuario':
                oferta = OfertaUsuario.objects.get(id=oferta_id)
            else:
                oferta = OfertaEmpresa.objects.get(id=oferta_id)
            
            oferta.incrementar_vistas()
            return True
        except (OfertaUsuario.DoesNotExist, OfertaEmpresa.DoesNotExist):
            return False