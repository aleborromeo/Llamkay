"""
Repositorio para Trabajos Guardados
Responsabilidad: Acceso a datos de trabajos guardados
"""
from typing import Optional
from django.db.models import QuerySet
from apps.jobs.models import GuardarTrabajo


class GuardadoRepository:
    """
    Repositorio para gestionar acceso a datos de trabajos guardados
    Principio de Responsabilidad Única (SOLID)
    """
    
    @staticmethod
    def get_by_id(guardado_id: int) -> Optional[GuardarTrabajo]:
        """Obtiene un trabajo guardado por ID"""
        try:
            return GuardarTrabajo.objects.select_related(
                'id_oferta_usuario',
                'id_oferta_empresa'
            ).get(id=guardado_id)
        except GuardarTrabajo.DoesNotExist:
            return None
    
    @staticmethod
    def existe_guardado(usuario_id: int, oferta_id: int, tipo_oferta: str) -> bool:
        """
        Verifica si un trabajo ya está guardado
        
        Args:
            usuario_id: ID del usuario
            oferta_id: ID de la oferta
            tipo_oferta: 'usuario' o 'empresa'
        """
        filtro = {'id_usuario_id': usuario_id}
        
        if tipo_oferta == 'usuario':
            filtro['id_oferta_usuario_id'] = oferta_id
        else:
            filtro['id_oferta_empresa_id'] = oferta_id
        
        return GuardarTrabajo.objects.filter(**filtro).exists()
    
    @staticmethod
    def get_guardados_usuario(usuario_id: int, limit: Optional[int] = None) -> QuerySet:
        """
        Obtiene todos los trabajos guardados de un usuario
        
        Args:
            usuario_id: ID del usuario
            limit: Límite opcional de resultados
        """
        queryset = GuardarTrabajo.objects.filter(
            id_usuario_id=usuario_id
        ).select_related(
            'id_oferta_usuario',
            'id_oferta_usuario__id_empleador',
            'id_oferta_usuario__id_categoria',
            'id_oferta_usuario__id_departamento',
            'id_oferta_usuario__id_provincia',
            'id_oferta_usuario__id_distrito',
            'id_oferta_empresa',
            'id_oferta_empresa__id_empleador',
            'id_oferta_empresa__id_categoria',
            'id_oferta_empresa__id_departamento',
            'id_oferta_empresa__id_provincia',
            'id_oferta_empresa__id_distrito',
        ).order_by('-created_at')
        
        if limit:
            queryset = queryset[:limit]
        
        return queryset
    
    @staticmethod
    def guardar_trabajo(data: dict) -> GuardarTrabajo:
        """
        Guarda un trabajo
        
        Args:
            data: Dict con id_usuario y id_oferta_usuario o id_oferta_empresa
        """
        return GuardarTrabajo.objects.create(**data)
    
    @staticmethod
    def eliminar_guardado(guardado_id: int, usuario_id: int) -> bool:
        """
        Elimina un trabajo guardado
        
        Args:
            guardado_id: ID del guardado
            usuario_id: ID del usuario (validación)
        """
        try:
            guardado = GuardarTrabajo.objects.get(
                id=guardado_id,
                id_usuario_id=usuario_id
            )
            guardado.delete()
            return True
        except GuardarTrabajo.DoesNotExist:
            return False
    
    @staticmethod
    def contar_guardados(usuario_id: int) -> int:
        """Cuenta los trabajos guardados de un usuario"""
        return GuardarTrabajo.objects.filter(id_usuario_id=usuario_id).count()
    
    @staticmethod
    def get_ids_guardados(usuario_id: int) -> set:
        """
        Obtiene los IDs de trabajos guardados para marcarlos en búsquedas
        
        Returns:
            Set con strings en formato "tipo_id" (ej: "usuario_123", "empresa_456")
        """
        guardados = GuardarTrabajo.objects.filter(
            id_usuario_id=usuario_id
        ).values('id_oferta_usuario_id', 'id_oferta_empresa_id')
        
        ids = set()
        for guardado in guardados:
            if guardado['id_oferta_usuario_id']:
                ids.add(f"usuario_{guardado['id_oferta_usuario_id']}")
            elif guardado['id_oferta_empresa_id']:
                ids.add(f"empresa_{guardado['id_oferta_empresa_id']}")
        
        return ids