# apps/users/repositories/factory.py
from apps.users.repositories.calificacion_repository import CalificacionRepository
from apps.users.repositories.decorators import LoggingRepositoryDecorator, SimpleCacheRepositoryDecorator


class RepositoryFactory:
    """
    Factory para centralizar creación + composición de repositorios.
    Permite cambiar wrappers sin tocar servicios ni vistas.
    """

    @staticmethod
    def calificacion_repo(use_logging: bool = True, use_cache: bool = False):
        repo = CalificacionRepository()

        # Orden recomendado: cache afuera o adentro es debatible.
        # Para demo: primero cache, luego logging (así loguea cache hits también).
        if use_cache:
            repo = SimpleCacheRepositoryDecorator(repo=repo)
        if use_logging:
            repo = LoggingRepositoryDecorator(repo=repo, label="CalificacionRepository")

        return repo
