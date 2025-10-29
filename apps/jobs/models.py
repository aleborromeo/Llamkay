"""
Modelos de Jobs - Corregido y Optimizado
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


# ==================== OFERTAS ====================
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
        return self.postulacion_set.count()

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
        return self.postulacion_set.count()

    def incrementar_vistas(self):
        """Incrementa contador de vistas"""
        self.vistas += 1
        self.save(update_fields=['vistas'])


# ==================== POSTULACIONES ====================
class Postulacion(models.Model):
    """
    Postulaciones de trabajadores a ofertas
    """
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En Revisión'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]

    id_postulacion = models.AutoField(primary_key=True)
    id_trabajador = models.ForeignKey(
        'users.Usuario', 
        on_delete=models.CASCADE,
        related_name='postulaciones_realizadas'
    )
    id_oferta_usuario = models.ForeignKey(
        OfertaUsuario, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='postulaciones'
    )
    id_oferta_empresa = models.ForeignKey(
        OfertaEmpresa, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='postulaciones'
    )
    
    # Información de la postulación
    mensaje = models.TextField(null=True, blank=True)
    pretension_salarial = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    disponibilidad_inmediata = models.BooleanField(default=False)
    
    # Estado
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    leida = models.BooleanField(default=False)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'postulacion'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['id_trabajador', 'estado']),
            models.Index(fields=['id_oferta_usuario', 'estado']),
            models.Index(fields=['id_oferta_empresa', 'estado']),
            models.Index(fields=['estado', '-created_at']),
        ]
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(id_oferta_usuario__isnull=False, id_oferta_empresa__isnull=True) |
                    models.Q(id_oferta_usuario__isnull=True, id_oferta_empresa__isnull=False)
                ),
                name='postulacion_una_oferta'
            )
        ]
        verbose_name = 'Postulación'
        verbose_name_plural = 'Postulaciones'

    def __str__(self):
        oferta = self.id_oferta_usuario or self.id_oferta_empresa
        return f"{self.id_trabajador.nombre_completo} -> {oferta}"

    @property
    def oferta(self):
        """Retorna la oferta relacionada"""
        return self.id_oferta_usuario or self.id_oferta_empresa

    @property
    def tipo_oferta(self):
        """Retorna el tipo de oferta"""
        return 'usuario' if self.id_oferta_usuario else 'empresa'

    def marcar_como_leida(self):
        """Marca la postulación como leída"""
        if not self.leida:
            self.leida = True
            self.save(update_fields=['leida'])


# ==================== CONTRATOS ====================
class Contrato(models.Model):
    """
    Contratos entre empleadores y trabajadores
    """
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('activo', 'Activo'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    id_contrato = models.AutoField(primary_key=True)
    id_empleador = models.ForeignKey(
        'users.Usuario',
        on_delete=models.RESTRICT,
        related_name='contratos_como_empleador'
    )
    id_trabajador = models.ForeignKey(
        'users.Usuario',
        on_delete=models.RESTRICT,
        related_name='contratos_como_trabajador'
    )
    id_postulacion = models.ForeignKey(
        Postulacion, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='contratos'
    )
    
    # Detalles del contrato
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    precio_acordado = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    moneda = models.CharField(max_length=3, default='PEN')
    
    # Fechas
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin_estimada = models.DateField(null=True, blank=True)
    fecha_fin_real = models.DateField(null=True, blank=True)
    
    # Estado
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contrato'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['id_empleador', 'estado']),
            models.Index(fields=['id_trabajador', 'estado']),
            models.Index(fields=['estado', '-created_at']),
        ]
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'

    def __str__(self):
        return f"Contrato #{self.id_contrato} - {self.titulo}"

    @property
    def esta_activo(self):
        """Verifica si el contrato está activo"""
        return self.estado == 'activo'


# ==================== PAGOS ====================
class Pago(models.Model):
    """
    Pagos asociados a contratos
    """
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('fallido', 'Fallido'),
        ('reembolsado', 'Reembolsado'),
    ]

    id_pago = models.AutoField(primary_key=True)
    id_contrato = models.ForeignKey(
        Contrato, 
        on_delete=models.RESTRICT,
        related_name='pagos'
    )
    
    # Montos
    monto_total = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    monto_trabajador = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    comision = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    moneda = models.CharField(max_length=3, default='PEN')
    
    # Estado
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pago'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['id_contrato', 'estado']),
            models.Index(fields=['estado', '-created_at']),
        ]
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'

    def __str__(self):
        return f"Pago #{self.id_pago} - {self.monto_total} {self.moneda}"


# ==================== CALIFICACIONES ====================
class Calificacion(models.Model):
    """
    Calificaciones mutuas entre empleadores y trabajadores
    """
    id_calificacion = models.AutoField(primary_key=True)
    id_contrato = models.ForeignKey(
        Contrato, 
        on_delete=models.CASCADE,
        related_name='calificaciones'
    )
    id_autor = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        related_name='calificaciones_dadas'
    )
    id_receptor = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        related_name='calificaciones_recibidas'
    )
    
    # Calificación
    puntuacion = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comentario = models.TextField(null=True, blank=True)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'calificacion'
        unique_together = [['id_contrato', 'id_autor']]
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['id_receptor', '-created_at']),
            models.Index(fields=['id_autor', '-created_at']),
        ]
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'

    def __str__(self):
        return f"Calificación {self.puntuacion}★ de {self.id_autor.nombre_completo}"


# ==================== TRABAJOS GUARDADOS ====================
class GuardarTrabajo(models.Model):
    """
    Trabajos guardados por los usuarios
    """
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        'users.Usuario', 
        on_delete=models.CASCADE,
        related_name='trabajos_guardados'
    )
    id_oferta_usuario = models.ForeignKey(
        OfertaUsuario, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='guardados'
    )
    id_oferta_empresa = models.ForeignKey(
        OfertaEmpresa, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='guardados'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'guardar_trabajo'
        ordering = ['-created_at']
        unique_together = [
            ['id_usuario', 'id_oferta_usuario'],
            ['id_usuario', 'id_oferta_empresa'],
        ]
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(id_oferta_usuario__isnull=False, id_oferta_empresa__isnull=True) |
                    models.Q(id_oferta_usuario__isnull=True, id_oferta_empresa__isnull=False)
                ),
                name='guardado_una_oferta'
            )
        ]
        indexes = [
            models.Index(fields=['id_usuario', '-created_at']),
        ]
        verbose_name = 'Trabajo Guardado'
        verbose_name_plural = 'Trabajos Guardados'

    def __str__(self):
        oferta = self.id_oferta_usuario or self.id_oferta_empresa
        return f"{self.id_usuario.nombre_completo} guardó {oferta}"

    @property
    def oferta(self):
        """Retorna la oferta guardada"""
        return self.id_oferta_usuario or self.id_oferta_empresa

    @property
    def tipo_oferta(self):
        """Retorna el tipo de oferta guardada"""
        return 'usuario' if self.id_oferta_usuario else 'empresa'