# apps/users/repositories/decorators.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional
import logging
import time

logger = logging.getLogger(__name__)


@dataclass
class RepositoryDecorator:
    """
    Decorator base para repositorios.
    Envuelve un repo real y delega llamadas.
    """
    repo: Any

    def __getattr__(self, item: str):
        # Delegar todo lo que no esté definido en el decorator
        return getattr(self.repo, item)


@dataclass
class LoggingRepositoryDecorator(RepositoryDecorator):
    """
    Agrega logging + timing sin cambiar el comportamiento del repo.
    """
    label: str = "repo"

    def _wrap(self, fn: Callable, *args, **kwargs):
        start = time.perf_counter()
        try:
            result = fn(*args, **kwargs)
            return result
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            logger.info("✅ %s.%s ejecutado en %.2fms", self.label, fn.__name__, elapsed_ms)

    # Ejemplo: interceptar llamadas “conocidas” (puedes agregar más si quieres)
    def listar_por_receptor(self, *args, **kwargs):
        return self._wrap(self.repo.listar_por_receptor, *args, **kwargs)

    def listar_por_autor(self, *args, **kwargs):
        return self._wrap(self.repo.listar_por_autor, *args, **kwargs)

    def obtener_por_contrato(self, *args, **kwargs):
        return self._wrap(self.repo.obtener_por_contrato, *args, **kwargs)

    def crear(self, *args, **kwargs):
        return self._wrap(self.repo.crear, *args, **kwargs)

    def actualizar(self, *args, **kwargs):
        return self._wrap(self.repo.actualizar, *args, **kwargs)

    def desactivar(self, *args, **kwargs):
        return self._wrap(self.repo.desactivar, *args, **kwargs)

    def calcular_estadisticas(self, *args, **kwargs):
        return self._wrap(self.repo.calcular_estadisticas, *args, **kwargs)

    def obtener_ultimas(self, *args, **kwargs):
        return self._wrap(self.repo.obtener_ultimas, *args, **kwargs)


@dataclass
class SimpleCacheRepositoryDecorator(RepositoryDecorator):
    """
    Cache en memoria (por request/proceso) para lecturas.
    NO cambia resultados, solo evita repetir queries.
    """
    _cache: Dict[str, Any] = None

    def __post_init__(self):
        if self._cache is None:
            self._cache = {}

    def _key(self, name: str, args: tuple, kwargs: dict) -> str:
        # Key simple (suficiente para demo). Puedes mejorar si deseas.
        return f"{name}|{args}|{sorted(kwargs.items())}"

    def listar_por_receptor(self, *args, **kwargs):
        k = self._key("listar_por_receptor", args, kwargs)
        if k in self._cache:
            return self._cache[k]
        res = self.repo.listar_por_receptor(*args, **kwargs)
        self._cache[k] = res
        return res

    def calcular_estadisticas(self, *args, **kwargs):
        k = self._key("calcular_estadisticas", args, kwargs)
        if k in self._cache:
            return self._cache[k]
        res = self.repo.calcular_estadisticas(*args, **kwargs)
        self._cache[k] = res
        return res

    def obtener_ultimas(self, *args, **kwargs):
        k = self._key("obtener_ultimas", args, kwargs)
        if k in self._cache:
            return self._cache[k]
        res = self.repo.obtener_ultimas(*args, **kwargs)
        self._cache[k] = res
        return res
