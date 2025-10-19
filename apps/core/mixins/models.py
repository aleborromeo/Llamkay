from django.db import models
from django.utils.text import slugify


class SlugMixin(models.Model):
    """Mixin para slug automático"""
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug and hasattr(self, 'nombre'):
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)


class ActiveMixin(models.Model):
    """Mixin para estado activo/inactivo"""
    is_active = models.BooleanField(default=True, verbose_name="¿Activo?")

    class Meta:
        abstract = True