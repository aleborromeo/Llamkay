from django.db import models
from django.contrib.auth.models import User

# ==================== UBICACIÓN ====================
class Departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    codigo = models.CharField(max_length=10, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'departamento'
        indexes = [models.Index(fields=['nombre'])]

    def __str__(self):
        return self.nombre


class Provincia(models.Model):
    id_provincia = models.AutoField(primary_key=True)
    id_departamento = models.ForeignKey(
        'Departamento', 
        on_delete=models.CASCADE,
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

    def __str__(self):
        return self.nombre


class Distrito(models.Model):
    id_distrito = models.AutoField(primary_key=True)
    id_provincia = models.ForeignKey(
        'Provincia',
        on_delete=models.CASCADE,
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

    def __str__(self):
        return self.nombre


class Comunidad(models.Model):
    id_comunidad = models.AutoField(primary_key=True)
    id_distrito = models.ForeignKey(
        'Distrito',
        on_delete=models.CASCADE,
        db_column='id_distrito'
    )
    nombre = models.CharField(max_length=100)
    latitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
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

    def __str__(self):
        return self.nombre


# ==================== USUARIO ====================
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
    
    id_usuario = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    
    # Información Personal
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    dni = models.CharField(max_length=20, unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    genero = models.CharField(max_length=20, choices=GENERO_CHOICES, null=True, blank=True)
    tipo_usuario = models.CharField(
        max_length=20, 
        choices=TIPO_USUARIO_CHOICES, 
        default='trabajador'
    )
    
    # Ubicación
    id_comunidad = models.ForeignKey(
        'Comunidad',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_comunidad'
    )
    direccion = models.TextField(null=True, blank=True)
    latitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    radio_km = models.IntegerField(default=10)
    
    # Estado y Verificación
    habilitado = models.BooleanField(default=True)
    estado_verificacion = models.CharField(
        max_length=20,
        choices=ESTADO_VERIFICACION_CHOICES,
        default='pendiente'
    )
    
    # Estadísticas
    rating_promedio = models.DecimalField(
        max_digits=3, 
        decimal_places=2, 
        default=0.00
    )
    total_calificaciones = models.IntegerField(default=0)
    trabajos_completados = models.IntegerField(default=0)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'usuario'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['tipo_usuario']),
            models.Index(fields=['latitud', 'longitud']),
            models.Index(fields=['estado_verificacion']),
            models.Index(fields=['habilitado'])
        ]

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    id_profile = models.AutoField(primary_key=True)
    id_usuario = models.OneToOneField(
        'Usuario',
        on_delete=models.CASCADE,
        db_column='id_usuario'
    )
    
    # Información Profesional
    bio = models.TextField(null=True, blank=True)
    ocupacion = models.CharField(max_length=100, null=True, blank=True)
    experiencia_anios = models.IntegerField(null=True, blank=True)
    tarifa_hora = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )
    foto_url = models.ImageField(
        upload_to='fotos_perfil/', 
        null=True, 
        blank=True
    )
    portafolio_url = models.URLField(max_length=500, null=True, blank=True)
    redes_sociales = models.JSONField(null=True, blank=True)
    
    # Ubicación Detallada
    id_departamento = models.ForeignKey(
        'Departamento',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_departamento'
    )
    id_provincia = models.ForeignKey(
        'Provincia',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_provincia'
    )
    id_distrito = models.ForeignKey(
        'Distrito',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_distrito'
    )
    id_comunidad = models.ForeignKey(
        'Comunidad',
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


# ==================== HABILIDADES ====================
class Habilidad(models.Model):
    NIVEL_CHOICES = [
        ('basico', 'Básico'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
        ('experto', 'Experto'),
    ]

    id_habilidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    categoria = models.CharField(max_length=50, null=True, blank=True)
    activa = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'habilidad'
        indexes = [
            models.Index(fields=['nombre']),
            models.Index(fields=['categoria', 'activa'])
        ]

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
        db_column='id_usuario'
    )
    id_habilidad = models.ForeignKey(
        'Habilidad',
        on_delete=models.CASCADE,
        db_column='id_habilidad'
    )
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='basico')
    anios_experiencia = models.IntegerField(null=True, blank=True)
    certificado = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuario_habilidad'
        unique_together = [['id_usuario', 'id_habilidad']]
        indexes = [
            models.Index(fields=['id_usuario', 'nivel']),
            models.Index(fields=['id_habilidad'])
        ]


# ==================== CATEGORÍAS ====================
class CategoriaTrabajo(models.Model):
    id_categoria = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True)
    id_padre = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_padre'
    )
    icono = models.CharField(max_length=50, null=True, blank=True)
    activa = models.BooleanField(default=True)
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

    def __str__(self):
        return self.nombre


class UsuarioCategoria(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,
        db_column='id_usuario'
    )
    id_categoria = models.ForeignKey(
        'CategoriaTrabajo',
        on_delete=models.CASCADE,
        db_column='id_categoria'
    )
    preferencia = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'usuario_categoria'
        unique_together = [['id_usuario', 'id_categoria']]
        indexes = [
            models.Index(fields=['id_usuario']),
            models.Index(fields=['id_categoria'])
        ]


# ==================== VERIFICACIÓN Y CERTIFICACIONES ====================
class Verificacion(models.Model):
    TIPO_VERIFICACION_CHOICES = [
        ('dni', 'DNI'),
        ('antecedentes', 'Antecedentes'),
        ('rostro', 'Rostro'),
        ('telefono', 'Teléfono'),
        ('email', 'Email'),
    ]

    ESTADO_VERIFICACION_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('verificado', 'Verificado'),
        ('rechazado', 'Rechazado'),
        ('expirado', 'Expirado'),
    ]

    id_verificacion = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,
        db_column='id_usuario'
    )
    tipo = models.CharField(max_length=20, choices=TIPO_VERIFICACION_CHOICES)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_VERIFICACION_CHOICES,
        default='pendiente'
    )
    
    # Archivos
    archivo_url = models.CharField(max_length=500, null=True, blank=True)
    archivo_frontal = models.CharField(max_length=500, null=True, blank=True)
    archivo_posterior = models.CharField(max_length=500, null=True, blank=True)
    
    # Observaciones
    observaciones = models.TextField(null=True, blank=True)
    motivo_rechazo = models.TextField(null=True, blank=True)
    
    # Fechas
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    fecha_revision = models.DateTimeField(null=True, blank=True)
    fecha_expiracion = models.DateField(null=True, blank=True)
    
    # Revisor
    id_revisado_por = models.ForeignKey(
        'Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verificaciones_revisadas',
        db_column='id_revisado_por'
    )

    class Meta:
        db_table = 'verificacion'
        indexes = [
            models.Index(fields=['id_usuario', 'tipo', 'estado']),
            models.Index(fields=['estado', 'fecha_solicitud'])
        ]


class Certificacion(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,
        db_column='id_usuario'
    )
    
    titulo = models.CharField(max_length=255)
    institucion = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    archivo = models.CharField(max_length=500, null=True, blank=True)
    fecha_obtencion = models.DateField(null=True, blank=True)
    fecha_expiracion = models.DateField(null=True, blank=True)
    
    verificada = models.BooleanField(default=False)
    fecha_verificacion = models.DateTimeField(null=True, blank=True)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'certificacion'
        indexes = [
            models.Index(fields=['id_usuario', 'verificada']),
            models.Index(fields=['-fecha_obtencion'])
        ]


class TrabajosRealizados(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,
        db_column='id_usuario'
    )
    
    titulo = models.CharField(max_length=255)
    empresa = models.CharField(max_length=255, null=True, blank=True)
    rol = models.CharField(max_length=255, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    actualmente = models.BooleanField(default=False)
    
    referencias = models.TextField(null=True, blank=True)
    documentos = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'trabajos_realizados'
        indexes = [
            models.Index(fields=['id_usuario', '-fecha_inicio'])
        ]


# ==================== DISPONIBILIDAD ====================
class Disponibilidad(models.Model):
    id = models.AutoField(primary_key=True)
    id_trabajador = models.ForeignKey(
        'Usuario',
        on_delete=models.CASCADE,
        db_column='id_trabajador'
    )
    
    dia_semana = models.IntegerField()  # 0=Domingo, 1=Lunes, ..., 6=Sábado
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    activa = models.BooleanField(default=True)

    class Meta:
        db_table = 'disponibilidad'
        unique_together = [['id_trabajador', 'dia_semana', 'hora_inicio', 'hora_fin']]
        indexes = [
            models.Index(fields=['id_trabajador', 'dia_semana', 'activa'])
        ]