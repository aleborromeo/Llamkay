"""
Modelos de Ofertas de Trabajo
"""
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


class OfertaUsuario(models.Model):
    """
    Ofertas publicadas por usuarios individuales (empleadores)
    """
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('pausada', 'Pausada'),
        ('cerrada', 'Cerrada'),
        ('completada', 'Completada'),
    ]

    MODALIDAD_PAGO_CHOICES = [
        ('por_hora', 'Por Hora'),
        ('por_dia', 'Por Día'),
        ('por_proyecto', 'Por Proyecto'),
        ('semanal', 'Semanal'),
        ('mensual', 'Mensual'),
    ]

    id = models.AutoField(primary_key=True)
    id_empleador = models.ForeignKey(
        'users.Usuario', 
        on_delete=models.CASCADE,
        related_name='ofertas_publicadas'
    )
    id_categoria = models.ForeignKey(
        'users.CategoriaTrabajo', 
        on_delete=models.RESTRICT,
        related_name='ofertas_usuario'
    )
    
    # Descripción del trabajo
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    modalidad_pago = models.CharField(max_length=20, choices=MODALIDAD_PAGO_CHOICES)
    pago = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    moneda = models.CharField(max_length=3, default='PEN')
    
    # Ubicación
    id_departamento = models.ForeignKey(
        'users.Departamento', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    id_provincia = models.ForeignKey(
        'users.Provincia', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    id_distrito = models.ForeignKey(
        'users.Distrito', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    direccion_detalle = models.TextField(null=True, blank=True)
    
    # Fechas
    fecha_inicio_estimada = models.DateField(null=True, blank=True)
    fecha_limite = models.DateField(null=True, blank=True)
    
    # Estado y visibilidad
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='activa')
    urgente = models.BooleanField(default=False)
    vistas = models.IntegerField(default=0)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'oferta_usuario'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['estado', '-created_at']),
            models.Index(fields=['id_empleador', 'estado']),
            models.Index(fields=['id_categoria', 'estado']),
        ]
        verbose_name = 'Oferta de Usuario'
        verbose_name_plural = 'Ofertas de Usuarios'

    def __str__(self):
        return f"{self.titulo} - {self.id_empleador.nombre_completo}"

    @property
    def esta_activa(self):
        """Verifica si la oferta está activa"""
        return self.estado == 'activa'

    @property
    def total_postulaciones(self):
        """Cuenta el total de postulaciones"""
        return self.postulaciones.count()

    def incrementar_vistas(self):
        """Incrementa contador de vistas"""
        self.vistas += 1
        self.save(update_fields=['vistas'])


class OfertaEmpresa(models.Model):
    """
    Ofertas publicadas por empresas
    """
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('pausada', 'Pausada'),
        ('cerrada', 'Cerrada'),
        ('completada', 'Completada'),
    ]

    MODALIDAD_PAGO_CHOICES = [
        ('por_hora', 'Por Hora'),
        ('mensual', 'Mensual'),
        ('por_proyecto', 'Por Proyecto'),
    ]

    id = models.AutoField(primary_key=True)
    id_empleador = models.ForeignKey(
        'users.Usuario', 
        on_delete=models.CASCADE,
        related_name='ofertas_empresa_publicadas'
    )
    id_categoria = models.ForeignKey(
        'users.CategoriaTrabajo', 
        on_delete=models.RESTRICT,
        related_name='ofertas_empresa'
    )
    
    # Descripción del puesto
    titulo_puesto = models.CharField(max_length=255)
    descripcion = models.TextField()
    modalidad_pago = models.CharField(max_length=20, choices=MODALIDAD_PAGO_CHOICES)
    pago = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    moneda = models.CharField(max_length=3, default='PEN')
    
    # Detalles del empleo
    experiencia_requerida = models.CharField(max_length=100, null=True, blank=True)
    vacantes = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    
    # Ubicación
    id_departamento = models.ForeignKey(
        'users.Departamento', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    id_provincia = models.ForeignKey(
        'users.Provincia', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    id_distrito = models.ForeignKey(
        'users.Distrito', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    
    # Estado y visibilidad
    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='activa')
    vistas = models.IntegerField(default=0)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'oferta_empresa'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['estado', '-created_at']),
            models.Index(fields=['id_empleador', 'estado']),
            models.Index(fields=['id_categoria', 'estado']),
        ]
        verbose_name = 'Oferta de Empresa'
        verbose_name_plural = 'Ofertas de Empresas'

    def __str__(self):
        return f"{self.titulo_puesto} - {self.id_empleador.nombre_completo}"

    @property
    def esta_activa(self):
        """Verifica si la oferta está activa"""
        return self.estado == 'activa'

    @property
    def total_postulaciones(self):
        """Cuenta el total de postulaciones"""
        return self.postulaciones.count()

    def incrementar_vistas(self):
        """Incrementa contador de vistas"""
        self.vistas += 1
        self.save(update_fields=['vistas'])