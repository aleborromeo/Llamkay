"""
Implementación del Repositorio de Usuario
Desacopla la lógica de acceso a datos
"""

from django.db.models import Q, Prefetch
from apps.users.models import Usuario, Profile, UsuarioHabilidad


class UsuarioRepository:
    """
    Repositorio para operaciones de base de datos de Usuario
    """
    
    def obtener_por_id(self, id_usuario):
        """Obtener usuario por ID con relaciones"""
        try:
            return Usuario.objects.select_related(
                'id_comunidad',
                'profile_detalle',
                'estadisticas'
            ).prefetch_related(
                'habilidades',
                'categorias',
                'certificaciones'
            ).get(id_usuario=id_usuario)
        except Usuario.DoesNotExist:
            return None
    
    def obtener_por_user(self, user):
        """Obtener usuario por objeto User de Django"""
        try:
            return Usuario.objects.select_related(
                'id_comunidad'
            ).get(
                user=user,
                habilitado=True  # Solo usuarios activos
            )
        except Usuario.DoesNotExist:
            raise ValueError(f"No se encontró usuario para: {user.username}")
    
    def obtener_completo(self, id_usuario):
        """Obtener usuario con todas sus relaciones para perfil completo"""
        try:
            return Usuario.objects.select_related(
                'id_comunidad__id_distrito__id_provincia__id_departamento',
                'profile_detalle',
                'estadisticas'
            ).prefetch_related(
                Prefetch('habilidades', queryset=UsuarioHabilidad.objects.select_related('id_habilidad')),
                'categorias',
                'certificaciones',
                'calificaciones_recibidas__id_autor'
            ).get(
                id_usuario=id_usuario,
                habilitado=True
            )
        except Usuario.DoesNotExist:
            raise ValueError(f"Usuario {id_usuario} no encontrado")
    
    def buscar_usuarios(self, filtros):
        """
        Buscar usuarios con filtros dinámicos
        filtros puede contener: tipo_usuario, categoria, ubicacion, etc.
        """
        queryset = Usuario.objects.filter(
            habilitado=True,
            verificado=True
        ).select_related(
            'id_comunidad',
            'profile_detalle'
        )
        
        # Aplicar filtros
        if 'tipo_usuario' in filtros:
            queryset = queryset.filter(tipo_usuario=filtros['tipo_usuario'])
        
        if 'categoria' in filtros:
            queryset = queryset.filter(categorias__id_categoria=filtros['categoria'])
        
        if 'departamento' in filtros:
            queryset = queryset.filter(id_comunidad__id_distrito__id_provincia__id_departamento=filtros['departamento'])
        
        if 'busqueda' in filtros:
            busqueda = filtros['busqueda']
            queryset = queryset.filter(
                Q(nombres__icontains=busqueda) |
                Q(apellidos__icontains=busqueda)
            )
        
        return queryset.distinct()
    
    def actualizar_perfil(self, usuario, datos):
        """Actualizar datos del usuario"""
        try:
            for campo, valor in datos.items():
                if hasattr(usuario, campo):
                    setattr(usuario, campo, valor)
            usuario.save()
            return True
        except Exception as e:
            print(f"Error actualizando perfil: {str(e)}")
            return False
    
    def obtener_estadisticas(self, usuario):
        """Obtener estadísticas del usuario"""
        from apps.jobs.models import Contrato, Postulacion
        
        if hasattr(usuario, 'estadisticas'):
            return {
                'trabajos_completados': usuario.estadisticas.trabajos_completados or 0,
                'total_calificaciones': usuario.estadisticas.total_calificaciones or 0,
                'rating_promedio': usuario.estadisticas.rating_promedio or 0.0,
            }
        
        # Si no existe estadisticas, calcular manualmente
        trabajos = Contrato.objects.filter(
            Q(id_empleador=usuario) | Q(id_trabajador=usuario),
            estado='completado'
        ).count()
        
        calificaciones = usuario.calificaciones_recibidas.count()
        
        return {
            'trabajos_completados': trabajos,
            'total_calificaciones': calificaciones,
            'rating_promedio': usuario.rating_promedio or 0.0,
        }