"""
Servicio de Perfil
Responsabilidad: Lógica de negocio relacionada con perfiles
"""

from typing import Dict, Any, Optional
from django.contrib.auth.models import User

from apps.users.repositories import (
    UsuarioRepository,
    ProfileRepository,
    CalificacionRepository
)
from apps.users.models import (
    UsuarioHabilidad,
    Certificacion,
    TrabajosRealizados
)


class PerfilService:
    """
    Servicio para gestionar perfiles de usuario
    Usa inyección de dependencias (DIP)
    """
    
    def __init__(
        self,
        usuario_repo: Optional[UsuarioRepository] = None,
        profile_repo: Optional[ProfileRepository] = None,
        calificacion_repo: Optional[CalificacionRepository] = None
    ):
        """
        Inyección de dependencias
        Si no se proveen, se usan las implementaciones por defecto
        """
        self.usuario_repo = usuario_repo or UsuarioRepository()
        self.profile_repo = profile_repo or ProfileRepository()
        self.calificacion_repo = calificacion_repo or CalificacionRepository()
    
    def obtener_datos_completos(self, user: User) -> Dict[str, Any]:
        """
        Obtiene todos los datos del perfil de un usuario
        Coordina múltiples repositorios
        """
        # Obtener usuario
        usuario = self.usuario_repo.obtener_por_user(user)
        if not usuario:
            raise ValueError("Usuario no encontrado")
        
        # Obtener o crear profile
        profile, _ = self.profile_repo.obtener_o_crear(usuario)
        
        # Obtener habilidades
        habilidades = UsuarioHabilidad.objects.filter(
            id_usuario=usuario
        ).select_related('id_habilidad')
        
        # Obtener certificaciones
        certificaciones = Certificacion.objects.filter(
            id_usuario=usuario
        ).order_by('-fecha_subida')
        
        # Obtener trabajos realizados
        trabajos = TrabajosRealizados.objects.filter(
            id_usuario=usuario
        ).order_by('-fecha_inicio')
        
        # Obtener calificaciones
        calificaciones = self.calificacion_repo.listar_por_receptor(usuario)
        
        # Obtener disponibilidad
        disponibilidad = self._obtener_disponibilidad(usuario)
        
        # Obtener estadísticas
        from .estadistica_service import EstadisticaService
        estadistica_service = EstadisticaService()
        estadisticas = estadistica_service.calcular_usuario(usuario)
        
        return {
            'usuario': usuario,
            'profile': profile,
            'habilidades': [h.id_habilidad.nombre for h in habilidades],
            'habilidades_detalle': habilidades,
            'certificaciones': certificaciones,
            'trabajos_realizados': trabajos,
            'trabajos': trabajos,
            'calificaciones': calificaciones,
            'disponibilidad': disponibilidad,
            'precio_hora': profile.tarifa_hora,
            'estadisticas': estadisticas,
            'tipo_usuario': usuario.tipo_usuario,
        }
    
    def obtener_perfil_publico(self, usuario_id: int) -> Dict[str, Any]:
        """
        Obtiene datos del perfil público de un usuario
        Solo muestra información verificada y pública
        """
        usuario = self.usuario_repo.obtener_por_id(usuario_id)
        if not usuario or not usuario.habilitado:
            raise ValueError("Usuario no encontrado o deshabilitado")
        
        profile = self.profile_repo.obtener_por_usuario(usuario)
        
        # Solo certificaciones verificadas
        certificaciones = Certificacion.objects.filter(
            id_usuario=usuario,
            verificada=True
        ).order_by('-fecha_obtencion')
        
        # Solo habilidades
        habilidades = UsuarioHabilidad.objects.filter(
            id_usuario=usuario
        ).select_related('id_habilidad')
        
        # Últimas 10 calificaciones
        calificaciones = self.calificacion_repo.obtener_ultimas(usuario, limite=10)
        
        # Disponibilidad formateada
        disponibilidad = self._obtener_disponibilidad(usuario)
        
        return {
            'usuario': usuario,
            'profile': profile or {},
            'habilidades': [h.id_habilidad.nombre for h in habilidades],
            'certificaciones': certificaciones,
            'calificaciones': calificaciones,
            'disponibilidad': disponibilidad,
            'precio_hora': profile.tarifa_hora if profile else None,
        }
    
    def actualizar_perfil(self, user: User, datos: Dict[str, Any]) -> bool:
        """
        Actualiza el perfil de un usuario
        Valida y coordina actualizaciones
        """
        try:
            usuario = self.usuario_repo.obtener_por_user(user)
            if not usuario:
                return False
            
            # Actualizar datos básicos del usuario
            datos_usuario = {}
            if 'telefono' in datos:
                datos_usuario['telefono'] = datos['telefono']
            
            if datos_usuario:
                self.usuario_repo.actualizar(usuario, datos_usuario)
            
            # Actualizar profile
            profile, _ = self.profile_repo.obtener_o_crear(usuario)
            datos_profile = {}
            
            campos_profile = [
                'bio', 'ocupacion', 'experiencia_anios', 'tarifa_hora',
                'portafolio_url', 'id_departamento', 'id_provincia',
                'id_distrito', 'perfil_publico_activo', 'mostrar_email',
                'mostrar_telefono'
            ]
            
            for campo in campos_profile:
                if campo in datos:
                    datos_profile[campo] = datos[campo]
            
            if 'foto' in datos:
                datos_profile['foto_url'] = datos['foto']
            
            if 'descripcion' in datos:
                datos_profile['bio'] = datos['descripcion']
            
            if datos_profile:
                self.profile_repo.actualizar(profile, datos_profile)
            
            return True
            
        except Exception as e:
            print(f"Error al actualizar perfil: {str(e)}")
            return False
    
    def _obtener_disponibilidad(self, usuario) -> Optional[str]:
        """
        Obtiene y formatea la disponibilidad del usuario
        Método privado interno
        """
        if not hasattr(usuario, 'disponibilidad_set'):
            return None
        
        disponibilidades = usuario.disponibilidad_set.filter(activa=True)
        if not disponibilidades.exists():
            return None
        
        # Formatear horarios
        dias = {
            0: 'Dom', 1: 'Lun', 2: 'Mar', 3: 'Mié',
            4: 'Jue', 5: 'Vie', 6: 'Sáb'
        }
        
        horarios = [
            f"{dias[d.dia_semana]} {d.hora_inicio.strftime('%H:%M')}-{d.hora_fin.strftime('%H:%M')}"
            for d in disponibilidades[:3]
        ]
        
        return ", ".join(horarios) if horarios else None
    
    def exportar_portafolio(self, user: User) -> Dict[str, Any]:
        """
        Prepara datos para exportar portafolio (PDF)
        """
        datos = self.obtener_datos_completos(user)
        
        # Agregar información adicional para el PDF
        usuario = datos['usuario']
        
        return {
            'usuario': usuario,
            'profile': datos['profile'],
            'habilidades': datos['habilidades'],
            'certificaciones': datos['certificaciones'],
            'trabajos': datos['trabajos_realizados'],
            'calificaciones': datos['calificaciones'],
            'estadisticas': datos['estadisticas'],
        }