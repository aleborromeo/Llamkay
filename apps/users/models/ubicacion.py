"""
Modelos de Ubicación Geográfica - Simplificado
"""
from django.db import models


class Departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'departamento'
        verbose_name = 'Departamento'
        verbose_name_plural = 'Departamentos'

    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    id_provincia = models.AutoField(primary_key=True)
    id_departamento = models.ForeignKey(
        Departamento,
        on_delete=models.CASCADE,
        related_name='provincias'
    )
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'provincia'
        unique_together = [['id_departamento', 'nombre']]
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'

    def __str__(self):
        return f"{self.nombre}, {self.id_departamento.nombre}"


class Distrito(models.Model):
    id_distrito = models.AutoField(primary_key=True)
    id_provincia = models.ForeignKey(
        Provincia,
        on_delete=models.CASCADE,
        related_name='distritos'
    )
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        db_table = 'distrito'
        unique_together = [['id_provincia', 'nombre']]
        verbose_name = 'Distrito'
        verbose_name_plural = 'Distritos'

    def __str__(self):
        return f"{self.nombre}, {self.id_provincia.nombre}"


class Comunidad(models.Model):
    id_comunidad = models.AutoField(primary_key=True)
    id_distrito = models.ForeignKey(
        Distrito,
        on_delete=models.CASCADE,
        related_name='comunidades'
    )
    nombre = models.CharField(max_length=100)
    latitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)

    class Meta:
        db_table = 'comunidad'
        unique_together = [['id_distrito', 'nombre']]
        verbose_name = 'Comunidad'
        verbose_name_plural = 'Comunidades'

    def __str__(self):
        return f"{self.nombre}, {self.id_distrito.nombre}"