"""
Modelo Usuario Core
Responsabilidad: Información esencial del usuario
"""

from django.db import models
from django.contrib.auth.models import User
from .ubicacion import Comunidad


class Usuario(models.Model):
    """
    Usuario Core - Solo información esencial
    """
    
    # Constantes
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

    ESTADO_VERIFICACION_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('verificado', 'Verificado'),
        ('rechazado', 'Rechazado'),
        ('expirado', 'Expirado'),
    ]

    # Relación con Django User
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='perfil'
    )
    
    # Identificación
    id_usuario = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True, db_index=True)
    email = models.EmailField(max_length=254, unique=True, db_index=True)
    
    # Información Personal Básica
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    dni = models.CharField(
        max_length=20, 
        unique=True, 
        null=True, 
        blank=True,
        db_index=True
    )
    telefono = models.CharField(max_length=20, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(
        max_length=20, 
        choices=GENERO_CHOICES, 
        null=True, 
        blank=True
    )
    
    # Tipo de Usuario
    tipo_usuario = models.CharField(
        max_length=20,
        choices=TIPO_USUARIO_CHOICES,
        default='trabajador',
        db_index=True
    )
    
    # Ubicación Básica
    id_comunidad = models.ForeignKey(
        Comunidad,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios',
        db_column='id_comunidad'
    )
    direccion = models.TextField(null=True, blank=True)
    latitud = models.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        null=True, 
        blank=True
    )
    longitud = models.DecimalField(
        max_digits=10, 
        decimal_places=7, 
        null=True, 
        blank=True
    )
    radio_km = models.IntegerField(
        default=10,
        help_text="Radio de búsqueda en kilómetros"
    )
    
    # Estado
    habilitado = models.BooleanField(default=True, db_index=True)
    estado_verificacion = models.CharField(
        max_length=20,
        choices=ESTADO_VERIFICACION_CHOICES,
        default='pendiente',
        db_index=True
    )
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'usuario'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['tipo_usuario', 'habilitado']),
            models.Index(fields=['latitud', 'longitud']),
            models.Index(fields=['estado_verificacion']),
        ]
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    @property
    def nombre_completo(self):
        """Retorna el nombre completo del usuario"""
        return f"{self.nombres} {self.apellidos}"

    @property
    def es_trabajador(self):
        """Verifica si el usuario es trabajador"""
        return self.tipo_usuario in ['trabajador', 'ambos']

    @property
    def es_empleador(self):
        """Verifica si el usuario es empleador"""
        return self.tipo_usuario in ['empleador', 'ambos', 'empresa']

    @property
    def esta_verificado(self):
        """Verifica si el usuario está verificado"""
        return self.estado_verificacion == 'verificado'

    def activar(self):
        """Activa el usuario"""
        self.habilitado = True
        self.save(update_fields=['habilitado'])

    def desactivar(self):
        """Desactiva el usuario"""
        self.habilitado = False
        self.save(update_fields=['habilitado'])