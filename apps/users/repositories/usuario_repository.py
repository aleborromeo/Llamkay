"""
Implementación del Repositorio de Usuario
Desacopla la lógica de acceso a datos
"""

from typing import List, Optional, Dict, Any
from django.db.models import Q
from django.contrib.auth.models import User

from apps.users.models import Usuario
from .interfaces import IUsuarioRepository


class UsuarioRepository(IUsuarioRepository):
    """
    Repositorio concreto para Usuario
    Implementa la interfaz IUsuarioRepository
    """
    
    def obtener_por_id(self, usuario_id: int) -> Optional[Usuario]:
        """Obtiene un usuario por ID"""
        try:
            return Usuario.objects.select_related('user', 'id_comunidad').get(
                id_usuario=usuario_id,
                deleted_at__isnull=True
            )
        except Usuario.DoesNotExist:
            return None
    
    def obtener_por_user(self, user: User) -> Optional[Usuario]:
        """Obtiene un usuario por objeto User de Django"""
        try:
            return Usuario.objects.select_related('id_comunidad').get(
                user=user,
                deleted_at__isnull=True
            )
        except Usuario.DoesNotExist:
            return None
    
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        """Obtiene un usuario por email"""
        try:
            return Usuario.objects.select_related('user').get(
                email=email,
                deleted_at__isnull=True
            )
        except Usuario.DoesNotExist:
            return None
    
    def obtener_por_dni(self, dni: str) -> Optional[Usuario]:
        """Obtiene un usuario por DNI"""
        try:
            return Usuario.objects.get(
                dni=dni,
                deleted_at__isnull=True
            )
        except Usuario.DoesNotExist:
            return None
    
    def crear(self, datos: Dict[str, Any]) -> Usuario:
        """Crea un nuevo usuario"""
        return Usuario.objects.create(**datos)
    
    def actualizar(self, usuario: Usuario, datos: Dict[str, Any]) -> Usuario:
        """Actualiza un usuario existente"""
        for campo, valor in datos.items():
            if hasattr(usuario, campo):
                setattr(usuario, campo, valor)
        usuario.save()
        return usuario
    
    def listar_activos(self, tipo_usuario: Optional[str] = None) -> List[Usuario]:
        """Lista usuarios activos, opcionalmente filtrados por tipo"""
        queryset = Usuario.objects.filter(
            habilitado=True,
            deleted_at__isnull=True
        ).select_related('id_comunidad')
        
        if tipo_usuario:
            queryset = queryset.filter(tipo_usuario=tipo_usuario)
        
        return list(queryset.order_by('-created_at'))
    
    def buscar(self, query: str, tipo: Optional[str] = None) -> List[Usuario]:
        """Busca usuarios por nombre o habilidades"""
        queryset = Usuario.objects.filter(
            habilitado=True,
            deleted_at__isnull=True
        )
        
        if tipo and tipo != 'todos':
            queryset = queryset.filter(tipo_usuario=tipo)
        
        if query:
            queryset = queryset.filter(
                Q(nombres__icontains=query) |
                Q(apellidos__icontains=query) |
                Q(username__icontains=query)
            )
        
        # Ordenar por rating y total de calificaciones
        return list(
            queryset.select_related('id_comunidad')
            .order_by('-estadisticas__rating_promedio', '-estadisticas__total_calificaciones')[:20]
        )
    
    def existe_email(self, email: str) -> bool:
        """Verifica si existe un email"""
        return Usuario.objects.filter(email=email).exists()
    
    def existe_dni(self, dni: str) -> bool:
        """Verifica si existe un DNI"""
        return Usuario.objects.filter(dni=dni).exists()
    
    def activar(self, usuario_id: int) -> bool:
        """Activa un usuario"""
        try:
            usuario = self.obtener_por_id(usuario_id)
            if usuario:
                usuario.activar()
                return True
            return False
        except Exception:
            return False
    
    def desactivar(self, usuario_id: int) -> bool:
        """Desactiva un usuario"""
        try:
            usuario = self.obtener_por_id(usuario_id)
            if usuario:
                usuario.desactivar()
                return True
            return False
        except Exception:
            return False