"""
Servicio de Trabajos Guardados
Responsabilidad: Lógica de negocio para guardar/quitar trabajos
"""
from typing import Dict, List
from apps.jobs.repositories import GuardadoRepository, OfertaRepository


class GuardadoService:
    """
    Servicio para gestión de trabajos guardados
    Principio de Responsabilidad Única (SOLID)
    """
    
    def __init__(self):
        self.guardado_repo = GuardadoRepository()
        self.oferta_repo = OfertaRepository()
    
    def guardar_trabajo(
        self,
        usuario_id: int,
        oferta_id: int,
        tipo_oferta: str
    ) -> Dict:
        """
        Guarda un trabajo
        
        Args:
            usuario_id: ID del usuario
            oferta_id: ID de la oferta
            tipo_oferta: 'usuario' o 'empresa'
        
        Returns:
            Dict con 'success' y 'message'
        """
        # Validar que la oferta existe y está activa
        if tipo_oferta == 'usuario':
            oferta = self.oferta_repo.get_oferta_usuario_by_id(oferta_id)
        else:
            oferta = self.oferta_repo.get_oferta_empresa_by_id(oferta_id)
        
        if not oferta:
            return {'success': False, 'message': 'Oferta no encontrada'}
        
        if oferta.estado != 'activa':
            return {'success': False, 'message': 'La oferta no está activa'}
        
        # Verificar que no esté ya guardado
        if self.guardado_repo.existe_guardado(usuario_id, oferta_id, tipo_oferta):
            return {'success': False, 'message': 'Ya has guardado esta oferta'}
        
        # Guardar
        datos = {'id_usuario_id': usuario_id}
        
        if tipo_oferta == 'usuario':
            datos['id_oferta_usuario_id'] = oferta_id
        else:
            datos['id_oferta_empresa_id'] = oferta_id
        
        self.guardado_repo.guardar_trabajo(datos)
        
        return {
            'success': True,
            'message': '✅ Trabajo guardado exitosamente'
        }
    
    def quitar_guardado(
        self,
        guardado_id: int,
        usuario_id: int
    ) -> Dict:
        """
        Quita un trabajo de guardados
        
        Args:
            guardado_id: ID del guardado
            usuario_id: ID del usuario (validación)
        
        Returns:
            Dict con 'success' y 'message'
        """
        if self.guardado_repo.eliminar_guardado(guardado_id, usuario_id):
            return {
                'success': True,
                'message': '✅ Trabajo eliminado de guardados'
            }
        
        return {
            'success': False,
            'message': 'No se pudo eliminar el trabajo'
        }
    
    def get_trabajos_guardados(self, usuario_id: int) -> List[Dict]:
        """
        Obtiene todos los trabajos guardados de un usuario
        
        Args:
            usuario_id: ID del usuario
        
        Returns:
            Lista de trabajos guardados formateados
        """
        guardados = self.guardado_repo.get_guardados_usuario(usuario_id)
        
        trabajos = []
        for guardado in guardados:
            if guardado.id_oferta_usuario:
                oferta = guardado.id_oferta_usuario
                trabajos.append({
                    'guardado_id': guardado.id,
                    'tipo': 'usuario',
                    'id': oferta.id,
                    'titulo': oferta.titulo,
                    'descripcion': oferta.descripcion,
                    'pago': oferta.pago,
                    'moneda': oferta.moneda,
                    'modalidad_pago': oferta.get_modalidad_pago_display(),
                    'fecha_guardado': guardado.created_at,
                    'fecha_publicacion': oferta.created_at,
                    'estado': oferta.estado,
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
                        'nombre': oferta.id_categoria.nombre if oferta.id_categoria else None,
                    },
                })
            elif guardado.id_oferta_empresa:
                oferta = guardado.id_oferta_empresa
                trabajos.append({
                    'guardado_id': guardado.id,
                    'tipo': 'empresa',
                    'id': oferta.id,
                    'titulo': oferta.titulo_puesto,
                    'descripcion': oferta.descripcion,
                    'pago': oferta.pago,
                    'moneda': oferta.moneda,
                    'modalidad_pago': oferta.get_modalidad_pago_display(),
                    'experiencia_requerida': oferta.experiencia_requerida,
                    'vacantes': oferta.vacantes,
                    'fecha_guardado': guardado.created_at,
                    'fecha_publicacion': oferta.created_at,
                    'estado': oferta.estado,
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
                        'nombre': oferta.id_categoria.nombre if oferta.id_categoria else None,
                    },
                })
        
        return trabajos
    
    def contar_guardados(self, usuario_id: int) -> int:
        """
        Cuenta los trabajos guardados
        
        Args:
            usuario_id: ID del usuario
        
        Returns:
            Número de trabajos guardados
        """
        return self.guardado_repo.contar_guardados(usuario_id)