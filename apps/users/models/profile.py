"""
Modelo Profile y Estadísticas
Responsabilidad: Información profesional y estadísticas del usuario
"""

from django.db import models
from django.contrib.auth.models import User
from .usuario import Usuario
from .ubicacion import Departamento, Provincia, Distrito, Comunidad


class Profile(models.Model):
    """
    Perfil Profesional del Usuario
    Separado del modelo Usuario para cumplir SRP
    """
    
    # Relaciones
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    id_profile = models.AutoField(primary_key=True)
    id_usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='profile_detalle',
        db_column='id_usuario'
    )
    
    # Información Profesional
    bio = models.TextField(
        null=True,
        blank=True,
        help_text="Descripción profesional del usuario"
    )
    ocupacion = models.CharField(max_length=100, null=True, blank=True)
    experiencia_anios = models.IntegerField(
        null=True,
        blank=True,
        help_text="Años de experiencia"
    )
    tarifa_hora = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Tarifa por hora en soles"
    )
    
    # Medios
    foto_url = models.ImageField(
        upload_to='fotos_perfil/',
        null=True,
        blank=True
    )
    portafolio_url = models.URLField(
        max_length=500,
        null=True,
        blank=True
    )
    redes_sociales = models.JSONField(
        null=True,
        blank=True,
        help_text="JSON con enlaces a redes sociales"
    )
    
    # Ubicación Detallada (para búsquedas)
    id_departamento = models.ForeignKey(
        Departamento,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_departamento'
    )
    id_provincia = models.ForeignKey(
        Provincia,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_provincia'
    )
    id_distrito = models.ForeignKey(
        Distrito,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_distrito'
    )
    id_comunidad = models.ForeignKey(
        Comunidad,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_comunidad'
    )
    
    # Privacidad
    perfil_publico_activo = models.BooleanField(default=True)
    mostrar_email = models.BooleanField(default=False)
    mostrar_telefono = models.BooleanField(default=False)
    
    # Auditoría
    fecha_registro = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'profile'
        indexes = [
            models.Index(fields=['id_usuario']),
            models.Index(fields=['id_departamento', 'id_provincia', 'id_distrito'])
        ]
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'

    def __str__(self):
        return f"Perfil de {self.id_usuario.nombre_completo}"


class UsuarioEstadisticas(models.Model):
    """
    Estadísticas calculadas del usuario
    Separado para no mezclar datos con cálculos
    """
    
    id_estadistica = models.AutoField(primary_key=True)
    id_usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='estadisticas',
        db_column='id_usuario'
    )
    
    # Calificaciones
    rating_promedio = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00
    )
    total_calificaciones = models.IntegerField(default=0)
    
    # Trabajos
    trabajos_completados = models.IntegerField(default=0)
    trabajos_activos = models.IntegerField(default=0)
    trabajos_cancelados = models.IntegerField(default=0)
    
    # Financiero
    ingresos_totales = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    ingresos_mes_actual = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    
    # Tiempos
    tiempo_respuesta_promedio = models.IntegerField(
        default=0,
        help_text="Tiempo promedio de respuesta en minutos"
    )
    
    # Auditoría
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'usuario_estadisticas'
        verbose_name = 'Estadística de Usuario'
        verbose_name_plural = 'Estadísticas de Usuarios'

    def __str__(self):
        return f"Estadísticas de {self.id_usuario.nombre_completo}"

    def actualizar_rating(self, nuevo_promedio, total):
        """Actualiza el rating del usuario"""
        self.rating_promedio = nuevo_promedio
        self.total_calificaciones = total
        self.save(update_fields=['rating_promedio', 'total_calificaciones', 'ultima_actualizacion'])

    def incrementar_trabajos_completados(self):
        """Incrementa el contador de trabajos completados"""
        self.trabajos_completados += 1
        self.save(update_fields=['trabajos_completados', 'ultima_actualizacion'])