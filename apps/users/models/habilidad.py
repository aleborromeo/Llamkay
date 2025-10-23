"""
Modelos de Habilidades y Categorías
Responsabilidad: Gestionar habilidades y categorías de trabajo
"""

from django.db import models
from .usuario import Usuario


class Habilidad(models.Model):
    """Habilidad o Competencia"""
    
    NIVEL_CHOICES = [
        ('basico', 'Básico'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
        ('experto', 'Experto'),
    ]

    id_habilidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True, db_index=True)
    descripcion = models.TextField(null=True, blank=True)
    categoria = models.CharField(max_length=50, null=True, blank=True)
    activa = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'habilidad'
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['categoria', 'activa'])
        ]
        verbose_name = 'Habilidad'
        verbose_name_plural = 'Habilidades'

    def __str__(self):
        return self.nombre


class UsuarioHabilidad(models.Model):
    """Relación entre Usuario y Habilidad"""
    
    NIVEL_CHOICES = [
        ('basico', 'Básico'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
        ('experto', 'Experto'),
    ]

    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='habilidades',
        db_column='id_usuario'
    )
    id_habilidad = models.ForeignKey(
        Habilidad,
        on_delete=models.CASCADE,
        related_name='usuarios',
        db_column='id_habilidad'
    )
    nivel = models.CharField(
        max_length=20,
        choices=NIVEL_CHOICES,
        default='basico'
    )
    anios_experiencia = models.IntegerField(
        null=True,
        blank=True,
        help_text="Años de experiencia con esta habilidad"
    )
    certificado = models.BooleanField(
        default=False,
        help_text="Si tiene certificación de esta habilidad"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuario_habilidad'
        unique_together = [['id_usuario', 'id_habilidad']]
        indexes = [
            models.Index(fields=['id_usuario', 'nivel']),
            models.Index(fields=['id_habilidad'])
        ]
        verbose_name = 'Habilidad de Usuario'
        verbose_name_plural = 'Habilidades de Usuarios'

    def __str__(self):
        return f"{self.id_usuario.nombre_completo} - {self.id_habilidad.nombre} ({self.nivel})"


class CategoriaTrabajo(models.Model):
    """Categoría de Trabajo"""
    
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True, db_index=True)
    descripcion = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    id_padre = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subcategorias',
        db_column='id_padre'
    )
    icono = models.CharField(max_length=50, null=True, blank=True)
    activa = models.BooleanField(default=True, db_index=True)
    orden = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categoria_trabajo'
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['activa', 'orden']),
            models.Index(fields=['id_padre'])
        ]
        verbose_name = 'Categoría de Trabajo'
        verbose_name_plural = 'Categorías de Trabajo'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return self.nombre


class UsuarioCategoria(models.Model):
    """Relación entre Usuario y Categoría"""
    
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='categorias',
        db_column='id_usuario'
    )
    id_categoria = models.ForeignKey(
        CategoriaTrabajo,
        on_delete=models.CASCADE,
        related_name='usuarios',
        db_column='id_categoria'
    )
    preferencia = models.BooleanField(
        default=False,
        help_text="Si es una categoría preferida del usuario"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuario_categoria'
        unique_together = [['id_usuario', 'id_categoria']]
        indexes = [
            models.Index(fields=['id_usuario']),
            models.Index(fields=['id_categoria'])
        ]
        verbose_name = 'Categoría de Usuario'
        verbose_name_plural = 'Categorías de Usuarios'

    def __str__(self):
        return f"{self.id_usuario.nombre_completo} - {self.id_categoria.nombre}"