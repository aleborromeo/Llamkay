"""
Implementación del Repositorio de Profile
"""

from typing import Optional, Dict, Any, Tuple

from apps.users.models import Profile, Usuario
from .interfaces import IProfileRepository


class ProfileRepository(IProfileRepository):
    """
    Repositorio concreto para Profile
    """
    
    def obtener_por_usuario(self, usuario: Usuario) -> Optional[Profile]:
        """Obtiene el perfil de un usuario"""
        try:
            return Profile.objects.select_related(
                'id_departamento',
                'id_provincia',
                'id_distrito',
                'id_comunidad'
            ).get(id_usuario=usuario)
        except Profile.DoesNotExist:
            return None
    
    def obtener_o_crear(self, usuario: Usuario) -> Tuple[Profile, bool]:
        """Obtiene o crea el perfil de un usuario"""
        return Profile.objects.get_or_create(
            id_usuario=usuario,
            user=usuario.user,
            defaults={
                'bio': '',
                'perfil_publico_activo': True
            }
        )
    
    def actualizar(self, profile: Profile, datos: Dict[str, Any]) -> Profile:
        """Actualiza un perfil"""
        for campo, valor in datos.items():
            if hasattr(profile, campo):
                setattr(profile, campo, valor)
        profile.save()
        return profile
    
    def actualizar_tarifa(self, usuario: Usuario, tarifa: float) -> bool:
        """Actualiza la tarifa por hora"""
        try:
            profile, _ = self.obtener_o_crear(usuario)
            profile.tarifa_hora = tarifa
            profile.save(update_fields=['tarifa_hora'])
            return True
        except Exception:
            return False
    
    def actualizar_foto(self, usuario: Usuario, foto) -> bool:
        """Actualiza la foto de perfil"""
        try:
            profile, _ = self.obtener_o_crear(usuario)
            profile.foto_url = foto
            profile.save(update_fields=['foto_url'])
            return True
        except Exception:
            return False
    
    def actualizar_bio(self, usuario: Usuario, bio: str) -> bool:
        """Actualiza la biografía"""
        try:
            profile, _ = self.obtener_o_crear(usuario)
            profile.bio = bio
            profile.save(update_fields=['bio'])
            return True
        except Exception:
            return False