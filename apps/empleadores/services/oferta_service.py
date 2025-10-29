"""
Servicio de Ofertas para Empleadores
Responsabilidad: Lógica de negocio para gestión de ofertas
"""
from typing import Dict, List, Optional
from apps.empleadores.repositories import OfertaEmpleadorRepository


class OfertaService:
    """
    Servicio para gestión de ofertas desde perspectiva del empleador
    Principio de Responsabilidad Única (SOLID)
    """
    
    def __init__(self):
        self.repository = OfertaEmpleadorRepository()
    
    def crear_oferta_individual(self, empleador_id: int, form_data: dict) -> Dict:
        """
        Crea una oferta individual
        
        Args:
            empleador_id: ID del empleador
            form_data: Datos del formulario
        
        Returns:
            Dict con 'success', 'message' y opcionalmente 'oferta'
        """
        try:
            # Preparar datos
            data = {
                'id_empleador_id': empleador_id,
                'estado': 'activa',
                **form_data
            }
            
            # Crear oferta
            oferta = self.repository.crear_oferta_usuario(data)
            
            return {
                'success': True,
                'message': '✅ Oferta publicada exitosamente',
                'oferta': oferta
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al crear oferta: {str(e)}'
            }
    
    def crear_oferta_empresa(self, empleador_id: int, form_data: dict) -> Dict:
        """
        Crea una oferta de empresa
        
        Args:
            empleador_id: ID del empleador
            form_data: Datos del formulario
        
        Returns:
            Dict con 'success', 'message' y opcionalmente 'oferta'
        """
        try:
            # Preparar datos
            data = {
                'id_empleador_id': empleador_id,
                'estado': 'activa',
                **form_data
            }
            
            # Crear oferta
            oferta = self.repository.crear_oferta_empresa(data)
            
            return {
                'success': True,
                'message': '✅ Oferta publicada exitosamente',
                'oferta': oferta
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al crear oferta: {str(e)}'
            }
    
    def actualizar_oferta(
        self,
        oferta_id: int,
        empleador_id: int,
        tipo: str,
        form_data: dict
    ) -> Dict:
        """
        Actualiza una oferta existente
        
        Args:
            oferta_id: ID de la oferta
            empleador_id: ID del empleador
            tipo: 'usuario' o 'empresa'
            form_data: Datos del formulario
        
        Returns:
            Dict con 'success' y 'message'
        """
        try:
            if tipo == 'usuario':
                exito = self.repository.actualizar_oferta_usuario(
                    oferta_id,
                    empleador_id,
                    form_data
                )
            else:
                exito = self.repository.actualizar_oferta_empresa(
                    oferta_id,
                    empleador_id,
                    form_data
                )
            
            if exito:
                return {
                    'success': True,
                    'message': '✅ Oferta actualizada correctamente'
                }
            else:
                return {
                    'success': False,
                    'message': 'Oferta no encontrada o sin permisos'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al actualizar oferta: {str(e)}'
            }
    
    def cambiar_estado(
        self,
        oferta_id: int,
        empleador_id: int,
        nuevo_estado: str,
        tipo: str
    ) -> Dict:
        """
        Cambia el estado de una oferta
        
        Args:
            oferta_id: ID de la oferta
            empleador_id: ID del empleador
            nuevo_estado: 'activa', 'pausada', 'cerrada'
            tipo: 'usuario' o 'empresa'
        
        Returns:
            Dict con 'success' y 'message'
        """
        estados_validos = ['activa', 'pausada', 'cerrada']
        
        if nuevo_estado not in estados_validos:
            return {
                'success': False,
                'message': 'Estado inválido'
            }
        
        exito = self.repository.cambiar_estado_oferta(
            oferta_id,
            empleador_id,
            nuevo_estado,
            tipo
        )
        
        if exito:
            return {
                'success': True,
                'message': f'Oferta {nuevo_estado} correctamente',
                'nuevo_estado': nuevo_estado
            }
        else:
            return {
                'success': False,
                'message': 'No se pudo cambiar el estado'
            }
    
    def get_mis_ofertas(self, empleador_id: int) -> Dict:
        """
        Obtiene todas las ofertas de un empleador
        
        Args:
            empleador_id: ID del empleador
        
        Returns:
            Dict con ofertas de usuario y empresa
        """
        ofertas_usuario = self.repository.get_ofertas_empleador_usuario(empleador_id)
        ofertas_empresa = self.repository.get_ofertas_empleador_empresa(empleador_id)
        
        return {
            'ofertas_usuario': ofertas_usuario,
            'ofertas_empresa': ofertas_empresa,
        }
    
    def get_oferta_para_editar(
        self,
        oferta_id: int,
        empleador_id: int
    ) -> Optional[tuple]:
        """
        Obtiene una oferta para editar, detectando automáticamente el tipo
        
        Args:
            oferta_id: ID de la oferta
            empleador_id: ID del empleador
        
        Returns:
            Tupla (oferta, tipo) o None si no existe
        """
        # Intentar como oferta de usuario
        oferta = self.repository.get_oferta_usuario_by_id_empleador(
            oferta_id,
            empleador_id
        )
        
        if oferta:
            return (oferta, 'usuario')
        
        # Intentar como oferta de empresa
        oferta = self.repository.get_oferta_empresa_by_id_empleador(
            oferta_id,
            empleador_id
        )
        
        if oferta:
            return (oferta, 'empresa')
        
        return None
    
    def get_estadisticas(self, empleador_id: int) -> Dict:
        """
        Obtiene estadísticas de ofertas del empleador
        
        Args:
            empleador_id: ID del empleador
        
        Returns:
            Dict con estadísticas
        """
        return self.repository.contar_ofertas_empleador(empleador_id)
    
    def get_ofertas_activas_recientes(
        self,
        empleador_id: int,
        limit: int = 5
    ) -> List[Dict]:
        """
        Obtiene las ofertas activas más recientes
        
        Args:
            empleador_id: ID del empleador
            limit: Límite de resultados
        
        Returns:
            Lista de ofertas formateadas
        """
        return self.repository.get_ofertas_activas_recientes(empleador_id, limit)