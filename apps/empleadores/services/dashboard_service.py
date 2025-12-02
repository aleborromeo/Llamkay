from typing import Dict, List
from apps.empleadores.repositories import OfertaEmpleadorRepository
from apps.jobs.repositories import PostulacionRepository


class DashboardService:
    
    def __init__(self):
        self.oferta_repo = OfertaEmpleadorRepository()
        self.postulacion_repo = PostulacionRepository()
    
    def get_estadisticas_dashboard(self, empleador_id: int) -> Dict:
        contadores_ofertas = self.oferta_repo.contar_ofertas_empleador(empleador_id)
        contadores_postulaciones = self.postulacion_repo.contar_postulaciones_empleador(empleador_id)
        
        return {
            **contadores_ofertas,
            **contadores_postulaciones,
        }
    
    def get_ofertas_recientes(self, empleador_id: int, limit: int = 5) -> List:
        return self.oferta_repo.get_ofertas_activas_recientes(empleador_id, limit)
    
    def get_postulaciones_recientes(self, empleador_id: int, limit: int = 10) -> List[Dict]:
        postulaciones = self.postulacion_repo.get_postulaciones_empleador(empleador_id)[:limit]
        
        postulaciones_data = []
        for post in postulaciones:
            oferta = post.oferta
            tipo = post.tipo_oferta
            
            postulaciones_data.append({
                'id': post.id_postulacion,
                'tipo': tipo,
                'titulo': oferta.titulo if tipo == 'usuario' else oferta.titulo_puesto,
                'trabajador': post.id_trabajador.nombre_completo,
                'estado': post.estado,
                'estado_display': post.get_estado_display(),
                'fecha': post.created_at,
                'leida': post.leida,
                'oferta_id': oferta.id,
            })
        
        return postulaciones_data