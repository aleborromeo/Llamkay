"""
Servicio de Verificación
Responsabilidad: Lógica de negocio para verificaciones y certificaciones
"""

from typing import Dict, Any, Optional, List
from django.core.files.uploadedfile import UploadedFile

from apps.users.models import Usuario, Verificacion, Certificacion


class VerificacionService:
    """
    Servicio para gestionar verificaciones y certificaciones
    """
    
    def solicitar_verificacion(
        self,
        usuario: Usuario,
        tipo: str,
        archivos: Dict[str, Any],
        observaciones: str = None
    ) -> Dict[str, Any]:
        """
        Solicita una verificación de identidad
        
        Args:
            usuario: Usuario que solicita la verificación
            tipo: Tipo de verificación ('dni', 'antecedentes', etc.)
            archivos: Dict con los archivos necesarios
            observaciones: Observaciones adicionales
            
        Returns:
            Dict con el resultado de la operación
        """
        try:
            # Validar que no exista una verificación pendiente del mismo tipo
            verificacion_existente = Verificacion.objects.filter(
                id_usuario=usuario,
                tipo=tipo,
                estado='pendiente'
            ).first()
            
            if verificacion_existente:
                return {
                    'success': False,
                    'error': f'Ya tienes una solicitud de verificación de {tipo} pendiente'
                }
            
            # Crear la verificación
            datos_verificacion = {
                'id_usuario': usuario,
                'tipo': tipo,
                'estado': 'pendiente',
                'observaciones': observaciones
            }
            
            # Agregar archivos según el tipo
            if tipo == 'dni':
                datos_verificacion['archivo_frontal'] = archivos.get('frontal')
                datos_verificacion['archivo_posterior'] = archivos.get('posterior')
            else:
                datos_verificacion['archivo_url'] = archivos.get('archivo')
            
            verificacion = Verificacion.objects.create(**datos_verificacion)
            
            return {
                'success': True,
                'message': 'Solicitud de verificación enviada correctamente',
                'verificacion_id': verificacion.id_verificacion
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al solicitar verificación: {str(e)}'
            }
    
    def aprobar_verificacion(
        self,
        verificacion_id: int,
        revisor: Usuario
    ) -> Dict[str, Any]:
        """
        Aprueba una verificación
        
        Args:
            verificacion_id: ID de la verificación
            revisor: Usuario que aprueba
            
        Returns:
            Dict con el resultado
        """
        try:
            verificacion = Verificacion.objects.get(id_verificacion=verificacion_id)
            verificacion.aprobar(revisor)
            
            # Actualizar estado del usuario si es verificación importante
            if verificacion.tipo in ['dni', 'antecedentes']:
                self._actualizar_estado_usuario(verificacion.id_usuario)
            
            return {
                'success': True,
                'message': 'Verificación aprobada correctamente'
            }
            
        except Verificacion.DoesNotExist:
            return {
                'success': False,
                'error': 'Verificación no encontrada'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al aprobar: {str(e)}'
            }
    
    def rechazar_verificacion(
        self,
        verificacion_id: int,
        revisor: Usuario,
        motivo: str
    ) -> Dict[str, Any]:
        """
        Rechaza una verificación
        
        Args:
            verificacion_id: ID de la verificación
            revisor: Usuario que rechaza
            motivo: Motivo del rechazo
            
        Returns:
            Dict con el resultado
        """
        try:
            verificacion = Verificacion.objects.get(id_verificacion=verificacion_id)
            verificacion.rechazar(revisor, motivo)
            
            return {
                'success': True,
                'message': 'Verificación rechazada'
            }
            
        except Verificacion.DoesNotExist:
            return {
                'success': False,
                'error': 'Verificación no encontrada'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al rechazar: {str(e)}'
            }
    
    def listar_verificaciones_usuario(
        self,
        usuario: Usuario
    ) -> List[Verificacion]:
        """
        Lista todas las verificaciones de un usuario
        
        Args:
            usuario: Usuario a consultar
            
        Returns:
            Lista de verificaciones
        """
        return list(
            Verificacion.objects.filter(
                id_usuario=usuario
            ).order_by('-fecha_solicitud')
        )
    
    def obtener_estado_verificacion(
        self,
        usuario: Usuario
    ) -> Dict[str, str]:
        """
        Obtiene el estado de todas las verificaciones del usuario
        
        Args:
            usuario: Usuario a consultar
            
        Returns:
            Dict con el estado de cada tipo de verificación
        """
        tipos = ['dni', 'antecedentes', 'rostro', 'telefono', 'email']
        estados = {}
        
        for tipo in tipos:
            verificacion = Verificacion.objects.filter(
                id_usuario=usuario,
                tipo=tipo
            ).order_by('-fecha_solicitud').first()
            
            if verificacion:
                estados[tipo] = verificacion.estado
            else:
                estados[tipo] = 'no_solicitado'
        
        return estados
    
    def _actualizar_estado_usuario(self, usuario: Usuario) -> None:
        """
        Actualiza el estado de verificación del usuario
        Método privado interno
        """
        # Verificar si tiene DNI y antecedentes verificados
        dni_verificado = Verificacion.objects.filter(
            id_usuario=usuario,
            tipo='dni',
            estado='verificado'
        ).exists()
        
        antecedentes_verificados = Verificacion.objects.filter(
            id_usuario=usuario,
            tipo='antecedentes',
            estado='verificado'
        ).exists()
        
        if dni_verificado and antecedentes_verificados:
            usuario.estado_verificacion = 'verificado'
            usuario.save(update_fields=['estado_verificacion'])
    
    # ==================== CERTIFICACIONES ====================
    
    def subir_certificacion(
        self,
        usuario: Usuario,
        titulo: str,
        institucion: str = None,
        descripcion: str = None,
        archivo: UploadedFile = None,
        fecha_obtencion = None,
        fecha_expiracion = None
    ) -> Dict[str, Any]:
        """
        Sube una certificación
        
        Args:
            usuario: Usuario propietario
            titulo: Título de la certificación
            institucion: Institución emisora
            descripcion: Descripción
            archivo: Archivo de la certificación
            fecha_obtencion: Fecha de obtención
            fecha_expiracion: Fecha de expiración
            
        Returns:
            Dict con el resultado
        """
        try:
            if not titulo:
                return {
                    'success': False,
                    'error': 'El título es obligatorio'
                }
            
            certificacion = Certificacion.objects.create(
                id_usuario=usuario,
                titulo=titulo,
                institucion=institucion,
                descripcion=descripcion,
                archivo=archivo,
                fecha_obtencion=fecha_obtencion,
                fecha_expiracion=fecha_expiracion
            )
            
            return {
                'success': True,
                'message': 'Certificación subida correctamente',
                'certificacion_id': certificacion.id
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al subir certificación: {str(e)}'
            }
    
    def verificar_certificacion(
        self,
        certificacion_id: int
    ) -> Dict[str, Any]:
        """
        Marca una certificación como verificada
        
        Args:
            certificacion_id: ID de la certificación
            
        Returns:
            Dict con el resultado
        """
        try:
            certificacion = Certificacion.objects.get(id=certificacion_id)
            certificacion.verificar()
            
            return {
                'success': True,
                'message': 'Certificación verificada correctamente'
            }
            
        except Certificacion.DoesNotExist:
            return {
                'success': False,
                'error': 'Certificación no encontrada'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al verificar: {str(e)}'
            }
    
    def listar_certificaciones_usuario(
        self,
        usuario: Usuario,
        solo_verificadas: bool = False
    ) -> List[Certificacion]:
        """
        Lista las certificaciones de un usuario
        
        Args:
            usuario: Usuario a consultar
            solo_verificadas: Si True, solo retorna verificadas
            
        Returns:
            Lista de certificaciones
        """
        queryset = Certificacion.objects.filter(id_usuario=usuario)
        
        if solo_verificadas:
            queryset = queryset.filter(verificada=True)
        
        return list(queryset.order_by('-fecha_obtencion'))
    
    def eliminar_certificacion(
        self,
        certificacion_id: int,
        usuario: Usuario
    ) -> Dict[str, Any]:
        """
        Elimina una certificación (solo el dueño puede eliminarla)
        
        Args:
            certificacion_id: ID de la certificación
            usuario: Usuario que solicita eliminar
            
        Returns:
            Dict con el resultado
        """
        try:
            certificacion = Certificacion.objects.get(
                id=certificacion_id,
                id_usuario=usuario
            )
            certificacion.delete()
            
            return {
                'success': True,
                'message': 'Certificación eliminada correctamente'
            }
            
        except Certificacion.DoesNotExist:
            return {
                'success': False,
                'error': 'Certificación no encontrada o no tienes permisos'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Error al eliminar: {str(e)}'
            }