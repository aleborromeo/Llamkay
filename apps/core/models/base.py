from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Modelo abstracto con timestamps"""
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Actualizado")

    class Meta:
        abstract = True
        ordering = ['-created_at']


class SoftDeleteModel(models.Model):
    """Modelo abstracto con eliminación lógica"""
    deleted_at = models.DateTimeField(null=True, blank=True, verbose_name="Eliminado")
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """Eliminación lógica"""
        self.deleted_at = timezone.now()
        self.is_deleted = True
        self.save(using=using)

    def hard_delete(self, using=None, keep_parents=False):
        """Eliminación física"""
        super().delete(using=using, keep_parents=keep_parents)


class BaseModel(TimeStampedModel, SoftDeleteModel):
    """Modelo base completo"""
    class Meta:
        abstract = True