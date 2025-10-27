"""
Modelo Usuario - Simplificado
"""
from django.db import models
from django.contrib.auth.models import User


class Usuario(models.Model):
    TIPO_USUARIO_CHOICES = [
        ('trabajador', 'Trabajador'),
        ('empleador', 'Empleador'),
        ('ambos', 'Ambos'),
        ('empresa', 'Empresa'),
    ]

    GENERO_CHOICES = [
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('otro', 'Otro'),
        ('prefiero_no_decir', 'Prefiero no decir'),
    ]

    # Relación con Django User
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    
    # Identificación
    id_usuario = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=254, unique=True)
    
    # Información Personal
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES, null=True, blank=True)
    
    # Tipo y Estado
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_USUARIO_CHOICES, default='trabajador')
    habilitado = models.BooleanField(default=True)
    verificado = models.BooleanField(default=False)
    
    # Ubicación
    id_comunidad = models.ForeignKey(
        'Comunidad',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios'
    )
    direccion = models.TextField(null=True, blank=True)
    latitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'usuario'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    @property
    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"