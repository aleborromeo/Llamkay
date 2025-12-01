"""
Modelos de Habilidades y Categorías - Simplificado
"""
from django.db import models


class Habilidad(models.Model):
    id_habilidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    activa = models.BooleanField(default=True)

    class Meta:
        db_table = 'habilidad'
        verbose_name = 'Habilidad'
        verbose_name_plural = 'Habilidades'

    def __str__(self):
        return self.nombre


class UsuarioHabilidad(models.Model):
    NIVEL_CHOICES = [
        ('basico', 'Básico'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
        ('experto', 'Experto'),
    ]

    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,
        related_name='habilidades'
    )
    id_habilidad = models.ForeignKey(
        Habilidad,
        on_delete=models.CASCADE,
        related_name='usuarios'
    )
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='basico')
    anios_experiencia = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuario_habilidad'
        unique_together = [['id_usuario', 'id_habilidad']]
        verbose_name = 'Habilidad de Usuario'
        verbose_name_plural = 'Habilidades de Usuarios'

    def __str__(self):
        return f"{self.id_usuario.nombre_completo} - {self.id_habilidad.nombre}"


class CategoriaTrabajo(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    icono = models.CharField(max_length=50, null=True, blank=True)
    activa = models.BooleanField(default=True)
    orden = models.IntegerField(default=0)

    class Meta:
        db_table = 'categoria_trabajo'
        verbose_name = 'Categoría de Trabajo'
        verbose_name_plural = 'Categorías de Trabajo'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre


class UsuarioCategoria(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,
        related_name='categorias'
    )
    id_categoria = models.ForeignKey(
        CategoriaTrabajo,
        on_delete=models.CASCADE,
        related_name='usuarios'
    )
    preferencia = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuario_categoria'
        unique_together = [['id_usuario', 'id_categoria']]
        verbose_name = 'Categoría de Usuario'
        verbose_name_plural = 'Categorías de Usuarios'

    def __str__(self):
        return f"{self.id_usuario.nombre_completo} - {self.id_categoria.nombre}"