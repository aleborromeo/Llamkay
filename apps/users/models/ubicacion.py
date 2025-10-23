"""
Modelos de Ubicación Geográfica
Responsabilidad: Gestionar la estructura geográfica del Perú
"""

from django.db import models


class Departamento(models.Model):
    """Departamento del Perú"""
    
    id_departamento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'departamento'
        indexes = [models.Index(fields=['nombre'])]
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    """Provincia del Perú"""
    
    id_provincia = models.AutoField(primary_key=True)
    id_departamento = models.ForeignKey(
        Departamento,
        on_delete=models.CASCADE,
        related_name='provincias',
        db_column='id_departamento'
    )
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'provincia'
        unique_together = [['id_departamento', 'nombre']]
        indexes = [
            models.Index(fields=['id_departamento']),
            models.Index(fields=['nombre'])
        ]
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'

    def __str__(self):
        return f"{self.nombre}, {self.id_departamento.nombre}"


class Distrito(models.Model):
    """Distrito del Perú"""
    
    id_distrito = models.AutoField(primary_key=True)
    id_provincia = models.ForeignKey(
        Provincia,
        on_delete=models.CASCADE,
        related_name='distritos',
        db_column='id_provincia'
    )
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'distrito'
        unique_together = [['id_provincia', 'nombre']]
        indexes = [
            models.Index(fields=['id_provincia']),
            models.Index(fields=['nombre'])
        ]
        verbose_name = 'Distrito'
        verbose_name_plural = 'Distritos'

    def __str__(self):
        return f"{self.nombre}, {self.id_provincia.nombre}"


class Comunidad(models.Model):
    """Comunidad o Centro Poblado"""
    
    id_comunidad = models.AutoField(primary_key=True)
    id_distrito = models.ForeignKey(
        Distrito,
        on_delete=models.CASCADE,
        related_name='comunidades',
        db_column='id_distrito'
    )
    nombre = models.CharField(max_length=100)
    latitud = models.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        null=True, 
        blank=True,
        help_text="Coordenada de latitud"
    )
    longitud = models.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        null=True, 
        blank=True,
        help_text="Coordenada de longitud"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'comunidad'
        unique_together = [['id_distrito', 'nombre']]
        indexes = [
            models.Index(fields=['id_distrito']),
            models.Index(fields=['nombre']),
            models.Index(fields=['latitud', 'longitud'])
        ]
        verbose_name = 'Comunidad'
        verbose_name_plural = 'Comunidades'

    def __str__(self):
        return f"{self.nombre}, {self.id_distrito.nombre}"