from abc import ABC, abstractmethod
from typing import Dict, Any
from django.db.models import Avg

from apps.jobs.models import Calificacion
from apps.users.models import Usuario


class RatingStatsStrategy(ABC):
    @abstractmethod
    def calcular(self, usuario: Usuario) -> Dict[str, Any]:
        pass


class DefaultRatingStatsStrategy(RatingStatsStrategy):
    def calcular(self, usuario: Usuario) -> Dict[str, Any]:
        qs = Calificacion.objects.filter(
            id_receptor=usuario,
            activa=True
        )

        total = qs.count()

        if total == 0:
            return {
                'total': 0,
                'promedio': 0.0,
                'estrellas': {i: 0 for i in range(1, 6)},
                'promedio_puntualidad': None,
                'promedio_calidad': None,
                'promedio_comunicacion': None,
            }

        # Promedio general
        promedio = round(qs.aggregate(avg=Avg('puntuacion'))['avg'] or 0.0, 2)

        # Conteo por estrellas
        estrellas = {i: 0 for i in range(1, 6)}
        for c in qs:
            if c.puntuacion in estrellas:
                estrellas[c.puntuacion] += 1

        # Promedios de aspectos (solo si existen)
        detalles = qs.aggregate(
            promedio_puntualidad=Avg('puntualidad'),
            promedio_calidad=Avg('calidad_trabajo'),
            promedio_comunicacion=Avg('comunicacion'),
        )

        return {
            'total': total,
            'promedio': promedio,
            'estrellas': estrellas,
            'promedio_puntualidad': round(detalles['promedio_puntualidad'], 1) if detalles['promedio_puntualidad'] is not None else None,
            'promedio_calidad': round(detalles['promedio_calidad'], 1) if detalles['promedio_calidad'] is not None else None,
            'promedio_comunicacion': round(detalles['promedio_comunicacion'], 1) if detalles['promedio_comunicacion'] is not None else None,
        }
