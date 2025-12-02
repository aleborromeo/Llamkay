"""
Servicio de Búsqueda de Trabajos
Responsabilidad: Lógica de negocio para búsqueda y visualización de ofertas
"""
from typing import List, Dict, Optional
from apps.jobs.repositories import OfertaRepository, PostulacionRepository, GuardadoRepository


class BusquedaService:
    """
    Servicio para búsqueda de trabajos
    Principio de Responsabilidad Única (SOLID)
    """
    
    def __init__(self):
        self.oferta_repo = OfertaRepository()
        self.postulacion_repo = PostulacionRepository()
        self.guardado_repo = GuardadoRepository()
    
    def buscar_trabajos(
        self,
        filtros: dict,
        usuario_actual=None
    ) -> List[Dict]:
        """
        Busca trabajos unificados (usuarios y empresas)
        
        Args:
            filtros: Dict con filtros de búsqueda
            usuario_actual: Usuario autenticado (opcional)
        
        Returns:
            Lista de trabajos en formato unificado
        """
        trabajos = []
        
        # Determinar qué tipo de ofertas buscar
        tipo = filtros.get('tipo')
        
        if tipo != 'empresa':
            # Buscar ofertas de usuario
            ofertas_usuario = self.oferta_repo.buscar_ofertas_usuario(
                filtros,
                excluir_empleador=usuario_actual
            )
            trabajos.extend(self._formatear_ofertas_usuario(ofertas_usuario))
        
        if tipo != 'empleador':
            # Buscar ofertas de empresa
            ofertas_empresa = self.oferta_repo.buscar_ofertas_empresa(
                filtros,
                excluir_empleador=usuario_actual
            )
            trabajos.extend(self._formatear_ofertas_empresa(ofertas_empresa))
        
        # Ordenar por fecha
        trabajos.sort(key=lambda x: x['fecha_publicacion'], reverse=True)
        
        return trabajos
    
    def get_detalle_trabajo(
        self,
        tipo: str,
        trabajo_id: int,
        usuario_actual=None
    ) -> Optional[Dict]:
        """
        Obtiene el detalle completo de un trabajo
        
        Args:
            tipo: 'usuario' o 'empresa'
            trabajo_id: ID del trabajo
            usuario_actual: Usuario autenticado (opcional)
        
        Returns:
            Dict con detalle del trabajo o None si no existe
        """
        # Obtener oferta
        if tipo == 'usuario':
            oferta = self.oferta_repo.get_oferta_usuario_by_id(trabajo_id)
        else:
            oferta = self.oferta_repo.get_oferta_empresa_by_id(trabajo_id)
        
        if not oferta or oferta.estado != 'activa':
            return None
        
        # Incrementar vistas
        self.oferta_repo.incrementar_vistas(trabajo_id, tipo)
        
        # Verificar información adicional si hay usuario
        ya_postulo = False
        es_guardado = False
        es_dueno = False
        
        if usuario_actual:
            es_dueno = (oferta.id_empleador.id_usuario == usuario_actual.id_usuario)
            
            if not es_dueno:
                ya_postulo = self.postulacion_repo.existe_postulacion(
                    usuario_actual.id_usuario,
                    trabajo_id,
                    tipo
                )
                
                es_guardado = self.guardado_repo.existe_guardado(
                    usuario_actual.id_usuario,
                    trabajo_id,
                    tipo
                )
        
        # Contar postulaciones activas
        total_postulaciones = oferta.postulaciones.filter(
            estado__in=['pendiente', 'en_revision', 'aceptada']
        ).count()
        
        return {
            'oferta': oferta,
            'tipo': tipo,
            'ya_postulo': ya_postulo,
            'es_guardado': es_guardado,
            'es_dueno': es_dueno,
            'total_postulaciones': total_postulaciones,
        }
    
    def marcar_trabajos_guardados(
        self,
        trabajos: List[Dict],
        usuario_id: int
    ) -> List[Dict]:
        """
        Marca qué trabajos están guardados por el usuario
        
        Args:
            trabajos: Lista de trabajos
            usuario_id: ID del usuario
        
        Returns:
            Lista de trabajos con marca de guardado
        """
        ids_guardados = self.guardado_repo.get_ids_guardados(usuario_id)
        
        for trabajo in trabajos:
            trabajo_key = f"{trabajo['tipo']}_{trabajo['id']}"
            trabajo['es_guardado'] = trabajo_key in ids_guardados
        
        return trabajos
    
    def marcar_trabajos_postulados(
        self,
        trabajos: List[Dict],
        usuario_id: int
    ) -> List[Dict]:
        """
        Marca a qué trabajos ya postuló el usuario
        
        Args:
            trabajos: Lista de trabajos
            usuario_id: ID del usuario
        
        Returns:
            Lista de trabajos con marca de postulación
        """
        for trabajo in trabajos:
            trabajo['ya_postulo'] = self.postulacion_repo.existe_postulacion(
                usuario_id,
                trabajo['id'],
                trabajo['tipo']
            )
        
        return trabajos
    
    def _formatear_ofertas_usuario(self, ofertas) -> List[Dict]:
        """Formatea ofertas de usuario a formato unificado"""
        trabajos = []
        
        for oferta in ofertas:
            trabajos.append({
                'tipo': 'usuario',
                'id': oferta.id,
                'titulo': oferta.titulo,
                'descripcion': oferta.descripcion,
                'pago': oferta.pago,
                'moneda': oferta.moneda,
                'modalidad_pago': oferta.get_modalidad_pago_display(),
                'fecha_publicacion': oferta.created_at,
                'fecha_limite': oferta.fecha_limite,
                'fecha_inicio_estimada': oferta.fecha_inicio_estimada,
                'urgente': oferta.urgente,
                'direccion_detalle': oferta.direccion_detalle,
                'empleador': {
                    'id': oferta.id_empleador.id_usuario,
                    'nombre': oferta.id_empleador.nombre_completo,
                },
                'ubicacion': {
                    'departamento': oferta.id_departamento.nombre if oferta.id_departamento else None,
                    'provincia': oferta.id_provincia.nombre if oferta.id_provincia else None,
                    'distrito': oferta.id_distrito.nombre if oferta.id_distrito else None,
                },
                'categoria': {
                    'id': oferta.id_categoria.id_categoria,
                    'nombre': oferta.id_categoria.nombre,
                } if oferta.id_categoria else None,
                'vistas': oferta.vistas,
                'postulaciones': oferta.postulaciones_count,
            })
        
        return trabajos
    
    def _formatear_ofertas_empresa(self, ofertas) -> List[Dict]:
        """Formatea ofertas de empresa a formato unificado"""
        trabajos = []
        
        for oferta in ofertas:
            trabajos.append({
                'tipo': 'empresa',
                'id': oferta.id,
                'titulo': oferta.titulo_puesto,
                'descripcion': oferta.descripcion,
                'pago': oferta.pago,
                'moneda': oferta.moneda,
                'modalidad_pago': oferta.get_modalidad_pago_display(),
                'experiencia_requerida': oferta.experiencia_requerida,
                'vacantes': oferta.vacantes,
                'fecha_publicacion': oferta.created_at,
                'empleador': {
                    'id': oferta.id_empleador.id_usuario,
                    'nombre': oferta.id_empleador.nombre_completo,
                },
                'ubicacion': {
                    'departamento': oferta.id_departamento.nombre if oferta.id_departamento else None,
                    'provincia': oferta.id_provincia.nombre if oferta.id_provincia else None,
                    'distrito': oferta.id_distrito.nombre if oferta.id_distrito else None,
                },
                'categoria': {
                    'id': oferta.id_categoria.id_categoria,
                    'nombre': oferta.id_categoria.nombre,
                } if oferta.id_categoria else None,
                'vistas': oferta.vistas,
                'postulaciones': oferta.postulaciones_count,
            })
        
        return trabajos