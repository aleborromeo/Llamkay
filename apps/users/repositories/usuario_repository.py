from typing import Any, Dict, List, Optional
from django.db.models import Q, Prefetch
from apps.users.models import Usuario, Profile, UsuarioHabilidad


class UsuarioRepository:
    """
    Repositorio para operaciones de base de datos de Usuario.
    Centraliza la lógica de acceso a datos para desacoplar el modelo.
    """

    # ----------------------------
    # 🔹 MÉTODOS DE OBTENCIÓN
    # ----------------------------
    
    def obtener_por_id(self, id_usuario: int) -> Optional[Usuario]:
        """Obtiene un usuario por ID con todas sus relaciones principales."""
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

    def obtener_por_user(self, user) -> Usuario:
        """Obtiene un usuario a partir del objeto User de Django."""
        try:
            return Usuario.objects.select_related(
                'id_comunidad'
            ).get(
                user=user,
                habilitado=True
            )
        except Usuario.DoesNotExist:
            raise ValueError(f"No se encontró usuario para: {user.username}")

    def obtener_completo(self, id_usuario: int) -> Usuario:
        """Obtiene el usuario con todas sus relaciones para el perfil completo."""
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

    def obtener_por_dni(self, dni: str) -> Optional[Usuario]:
        """Obtiene un usuario por DNI."""
        try:
            return Usuario.objects.get(dni=dni)
        except Usuario.DoesNotExist:
            return None

    # ----------------------------
    # 🔹 MÉTODOS DE CREACIÓN Y ACTUALIZACIÓN
    # ----------------------------

    def crear(self, datos: Dict[str, Any]) -> Usuario:
        """Crea un nuevo usuario."""
        return Usuario.objects.create(**datos)

    def actualizar(self, usuario: Usuario, datos: Dict[str, Any]) -> Usuario:
        """Actualiza un usuario existente con los datos proporcionados."""
        for campo, valor in datos.items():
            if hasattr(usuario, campo):
                setattr(usuario, campo, valor)
        usuario.save()
        return usuario

    def actualizar_perfil(self, usuario: Usuario, datos: Dict[str, Any]) -> bool:
        """Actualiza los datos del perfil del usuario."""
        try:
            for campo, valor in datos.items():
                if hasattr(usuario, campo):
                    setattr(usuario, campo, valor)
            usuario.save()
            return True
        except Exception as e:
            print(f"Error actualizando perfil: {str(e)}")
            return False

    # ----------------------------
    # 🔹 MÉTODOS DE CONSULTA Y BÚSQUEDA
    # ----------------------------

    def listar_activos(self, tipo_usuario: Optional[str] = None) -> List[Usuario]:
        """Lista todos los usuarios activos, opcionalmente filtrados por tipo."""
        queryset = Usuario.objects.filter(habilitado=True).select_related('id_comunidad')
        if tipo_usuario:
            queryset = queryset.filter(tipo_usuario=tipo_usuario)
        return list(queryset.order_by('-created_at'))

    def buscar_usuarios(self, filtros: Dict[str, Any]):
        """
        Busca usuarios con filtros dinámicos.
        Filtros posibles: tipo_usuario, categoria, departamento, busqueda, etc.
        """
        queryset = Usuario.objects.filter(
            habilitado=True,
            verificado=True
        ).select_related(
            'id_comunidad',
            'profile_detalle'
        )

        if 'tipo_usuario' in filtros:
            queryset = queryset.filter(tipo_usuario=filtros['tipo_usuario'])

        if 'categoria' in filtros:
            queryset = queryset.filter(categorias__id_categoria=filtros['categoria'])

        if 'departamento' in filtros:
            queryset = queryset.filter(
                id_comunidad__id_distrito__id_provincia__id_departamento=filtros['departamento']
            )

        if 'busqueda' in filtros:
            busqueda = filtros['busqueda']
            queryset = queryset.filter(
                Q(nombres__icontains=busqueda) |
                Q(apellidos__icontains=busqueda)
            )

        return queryset.distinct()

    # ----------------------------
    # 🔹 MÉTODOS DE ESTADÍSTICAS
    # ----------------------------

    def obtener_estadisticas(self, usuario: Usuario) -> Dict[str, Any]:
        """Obtiene o calcula las estadísticas del usuario."""
        from apps.jobs.models import Contrato

        if hasattr(usuario, 'estadisticas'):
            return {
                'trabajos_completados': usuario.estadisticas.trabajos_completados or 0,
                'total_calificaciones': usuario.estadisticas.total_calificaciones or 0,
                'rating_promedio': usuario.estadisticas.rating_promedio or 0.0,
            }

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
