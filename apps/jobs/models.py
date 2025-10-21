from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


# ==================== OFERTAS DE TRABAJO ====================
class OfertaUsuario(models.Model):
    ESTADO_OFERTA_CHOICES = [
        ('borrador', 'Borrador'),
        ('activa', 'Activa'),
        ('pausada', 'Pausada'),
        ('cerrada', 'Cerrada'),
        ('cancelada', 'Cancelada'),
    ]

    MODALIDAD_PAGO_CHOICES = [
        ('por_hora', 'Por Hora'),
        ('por_dia', 'Por Día'),
        ('por_proyecto', 'Por Proyecto'),
        ('mensual', 'Mensual'),
        ('semanal', 'Semanal'),
    ]

    id = models.AutoField(primary_key=True)
    id_empleador = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        db_column='id_empleador'
    )
    id_categoria = models.ForeignKey(
        'users.CategoriaTrabajo',
        on_delete=models.RESTRICT,
        db_column='id_categoria'
    )
    
    # Descripción del Trabajo
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    modalidad_pago = models.CharField(
        max_length=20,
        choices=MODALIDAD_PAGO_CHOICES
    )
    pago = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    moneda = models.CharField(max_length=3, default='PEN')
    
    # Ubicación
    id_departamento = models.ForeignKey(
        'users.Departamento',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_departamento'
    )
    id_provincia = models.ForeignKey(
        'users.Provincia',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_provincia'
    )
    id_distrito = models.ForeignKey(
        'users.Distrito',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_distrito'
    )
    id_comunidad = models.ForeignKey(
        'users.Comunidad',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_comunidad'
    )
    direccion_detalle = models.TextField(null=True, blank=True)
    latitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    radio_km = models.IntegerField(default=5)
    
    # Fechas y Tiempo
    fecha_inicio_estimada = models.DateField(null=True, blank=True)
    fecha_limite = models.DateField(null=True, blank=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    horas_limite = models.TimeField(null=True, blank=True)
    
    # Detalles Adicionales
    herramientas = models.TextField(null=True, blank=True)
    urgente = models.BooleanField(default=False)
    foto = models.CharField(max_length=500, null=True, blank=True)
    numero_contacto = models.CharField(max_length=15, null=True, blank=True)
    
    # Estado y Métricas
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_OFERTA_CHOICES,
        default='activa'
    )
    vistas = models.IntegerField(default=0)
    postulaciones_count = models.IntegerField(default=0)
    
    # Auditoría
    fecha_registro = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'oferta_usuario'
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['id_empleador', 'estado']),
            models.Index(fields=['id_categoria', 'estado', '-fecha_publicacion']),
            models.Index(fields=['urgente', 'estado']),
        ]


class OfertaEmpresa(models.Model):
    ESTADO_OFERTA_CHOICES = [
        ('borrador', 'Borrador'),
        ('activa', 'Activa'),
        ('pausada', 'Pausada'),
        ('cerrada', 'Cerrada'),
        ('cancelada', 'Cancelada'),
    ]

    MODALIDAD_PAGO_CHOICES = [
        ('por_hora', 'Por Hora'),
        ('por_dia', 'Por Día'),
        ('por_proyecto', 'Por Proyecto'),
        ('mensual', 'Mensual'),
        ('semanal', 'Semanal'),
    ]

    MODALIDAD_TRABAJO_CHOICES = [
        ('presencial', 'Presencial'),
        ('remoto', 'Remoto'),
        ('hibrido', 'Híbrido'),
    ]

    id = models.AutoField(primary_key=True)
    id_empleador = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        db_column='id_empleador'
    )
    id_categoria = models.ForeignKey(
        'users.CategoriaTrabajo',
        on_delete=models.RESTRICT,
        db_column='id_categoria'
    )
    
    # Descripción del Puesto
    titulo_puesto = models.CharField(max_length=255)
    descripcion = models.TextField()
    modalidad_pago = models.CharField(
        max_length=20,
        choices=MODALIDAD_PAGO_CHOICES
    )
    pago = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    moneda = models.CharField(max_length=3, default='PEN')
    
    # Detalles del Empleo
    rango_salarial = models.CharField(max_length=100, null=True, blank=True)
    experiencia_requerida = models.CharField(max_length=100, null=True, blank=True)
    modalidad_trabajo = models.CharField(
        max_length=20,
        choices=MODALIDAD_TRABAJO_CHOICES,
        default='presencial'
    )
    requisitos_calificaciones = models.TextField(null=True, blank=True)
    beneficios_compensaciones = models.TextField(null=True, blank=True)
    vacantes = models.IntegerField(default=1)
    
    # Ubicación
    id_departamento = models.ForeignKey(
        'users.Departamento',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_departamento'
    )
    id_provincia = models.ForeignKey(
        'users.Provincia',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_provincia'
    )
    id_distrito = models.ForeignKey(
        'users.Distrito',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_distrito'
    )
    id_comunidad = models.ForeignKey(
        'users.Comunidad',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_comunidad'
    )
    direccion_detalle = models.TextField(null=True, blank=True)
    latitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitud = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    radio_km = models.IntegerField(default=10)
    
    # Fechas
    fecha_inicio_estimada = models.DateField(null=True, blank=True)
    fecha_limite = models.DateField(null=True, blank=True)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    
    # Contacto
    foto = models.CharField(max_length=500, null=True, blank=True)
    numero_contacto = models.CharField(max_length=15, null=True, blank=True)
    
    # Estado y Métricas
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_OFERTA_CHOICES,
        default='activa'
    )
    vistas = models.IntegerField(default=0)
    postulaciones_count = models.IntegerField(default=0)
    
    # Auditoría
    fecha_registro = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'oferta_empresa'
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['id_empleador', 'estado']),
            models.Index(fields=['id_categoria', 'estado', '-fecha_publicacion']),
            models.Index(fields=['modalidad_trabajo', 'estado']),
        ]


# ==================== POSTULACIONES ====================
class Postulacion(models.Model):
    ESTADO_POSTULACION_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En Revisión'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
        ('retirada', 'Retirada'),
    ]

    id_postulacion = models.AutoField(primary_key=True)
    id_trabajador = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        db_column='id_trabajador'
    )
    id_oferta_usuario = models.ForeignKey(
        'OfertaUsuario',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column='id_oferta_usuario'
    )
    id_oferta_empresa = models.ForeignKey(
        'OfertaEmpresa',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column='id_oferta_empresa'
    )
    
    # Información de Postulación
    mensaje = models.TextField(null=True, blank=True)
    pretension_salarial = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    disponibilidad_inmediata = models.BooleanField(default=False)
    cv_adjunto = models.CharField(max_length=500, null=True, blank=True)
    
    # Estado
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_POSTULACION_CHOICES,
        default='pendiente'
    )
    leida = models.BooleanField(default=False)
    fecha_leida = models.DateTimeField(null=True, blank=True)
    
    # Auditoría
    fecha_postulacion = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'postulacion'
        unique_together = [
            ['id_trabajador', 'id_oferta_usuario'],
            ['id_trabajador', 'id_oferta_empresa']
        ]
        indexes = [
            models.Index(fields=['id_trabajador', 'estado']),
            models.Index(fields=['id_oferta_usuario', 'estado']),
            models.Index(fields=['id_oferta_empresa', 'estado']),
            models.Index(fields=['leida', '-fecha_postulacion']),
        ]


# ==================== CONTRATOS ====================
class Contrato(models.Model):
    ESTADO_CONTRATO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('activo', 'Activo'),
        ('en_pausa', 'En Pausa'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
        ('en_disputa', 'En Disputa'),
    ]

    id_contrato = models.AutoField(primary_key=True)
    id_empleador = models.ForeignKey(
        'users.Usuario',
        on_delete=models.RESTRICT,
        related_name='contratos_como_empleador',
        db_column='id_empleador'
    )
    id_trabajador = models.ForeignKey(
        'users.Usuario',
        on_delete=models.RESTRICT,
        related_name='contratos_como_trabajador',
        db_column='id_trabajador'
    )
    id_postulacion = models.ForeignKey(
        'Postulacion',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_postulacion'
    )
    id_oferta_usuario = models.ForeignKey(
        'OfertaUsuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_oferta_usuario'
    )
    id_oferta_empresa = models.ForeignKey(
        'OfertaEmpresa',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='id_oferta_empresa'
    )
    
    # Detalles del Contrato
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    precio_acordado = models.DecimalField(max_digits=10, decimal_places=2)
    moneda = models.CharField(max_length=3, default='PEN')
    modalidad_pago = models.CharField(max_length=20, null=True, blank=True)
    
    # Fechas
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin_estimada = models.DateField(null=True, blank=True)
    fecha_fin_real = models.DateField(null=True, blank=True)
    
    # Estado
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CONTRATO_CHOICES,
        default='pendiente'
    )
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contrato'
        indexes = [
            models.Index(fields=['id_empleador', 'estado']),
            models.Index(fields=['id_trabajador', 'estado']),
            models.Index(fields=['estado']),
            models.Index(fields=['fecha_inicio', 'fecha_fin_estimada']),
        ]


# ==================== SESIÓN DE TRABAJO ====================
class SesionTrabajo(models.Model):
    id_sesion = models.AutoField(primary_key=True)
    id_contrato = models.ForeignKey(
        'Contrato',
        on_delete=models.CASCADE,
        db_column='id_contrato'
    )
    
    fecha = models.DateField()
    hora_inicio = models.TimeField(null=True, blank=True)
    hora_fin = models.TimeField(null=True, blank=True)
    horas_trabajadas = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )
    nota = models.TextField(null=True, blank=True)
    aprobada = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sesion_trabajo'
        indexes = [
            models.Index(fields=['id_contrato', 'fecha']),
            models.Index(fields=['id_contrato', 'aprobada']),
        ]


# ==================== PAGOS ====================
class Pago(models.Model):
    METODO_PAGO_CHOICES = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia'),
        ('yape', 'Yape'),
        ('plin', 'Plin'),
        ('tarjeta', 'Tarjeta'),
        ('paypal', 'PayPal'),
    ]

    ESTADO_PAGO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('completado', 'Completado'),
        ('fallido', 'Fallido'),
        ('reembolsado', 'Reembolsado'),
    ]

    id_pago = models.AutoField(primary_key=True)
    id_contrato = models.ForeignKey(
        'Contrato',
        on_delete=models.RESTRICT,
        db_column='id_contrato'
    )
    
    # Montos
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    monto_trabajador = models.DecimalField(max_digits=10, decimal_places=2)
    comision_plataforma = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    moneda = models.CharField(max_length=3, default='PEN')
    
    # Método y Estado
    metodo_pago = models.CharField(
        max_length=20,
        choices=METODO_PAGO_CHOICES,
        null=True,
        blank=True
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_PAGO_CHOICES,
        default='pendiente'
    )
    
    # Referencias
    referencia_externa = models.CharField(max_length=255, null=True, blank=True)
    comprobante = models.CharField(max_length=500, null=True, blank=True)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    fecha_procesado = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'pago'
        indexes = [
            models.Index(fields=['id_contrato', 'estado']),
            models.Index(fields=['estado', '-created_at']),
            models.Index(fields=['fecha_procesado']),
        ]


# ==================== CALIFICACIONES ====================
class Calificacion(models.Model):
    ROL_CALIFICACION_CHOICES = [
        ('empleador', 'Empleador'),
        ('trabajador', 'Trabajador'),
    ]

    id_calificacion = models.AutoField(primary_key=True)
    id_contrato = models.ForeignKey(
        'Contrato',
        on_delete=models.CASCADE,
        db_column='id_contrato'
    )
    id_autor = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        related_name='calificaciones_dadas',
        db_column='id_autor'
    )
    id_receptor = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        related_name='calificaciones_recibidas',
        db_column='id_receptor'
    )
    rol_autor = models.CharField(max_length=20, choices=ROL_CALIFICACION_CHOICES)
    
    # Calificación
    puntuacion = models.IntegerField()  # 1-5
    comentario = models.TextField(null=True, blank=True)
    
    # Detalles
    puntualidad = models.IntegerField(null=True, blank=True)  # 1-5
    calidad_trabajo = models.IntegerField(null=True, blank=True)  # 1-5
    comunicacion = models.IntegerField(null=True, blank=True)  # 1-5
    
    # Estado
    activa = models.BooleanField(default=True)
    editada = models.BooleanField(default=False)
    
    # Auditoría
    fecha = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'calificacion'
        unique_together = [['id_contrato', 'id_autor']]
        indexes = [
            models.Index(fields=['id_receptor', 'activa']),
            models.Index(fields=['id_contrato']),
        ]


# ==================== TRABAJOS GUARDADOS ====================
class GuardarTrabajo(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        db_column='id_usuario'
    )
    id_oferta_usuario = models.ForeignKey(
        'OfertaUsuario',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column='id_oferta_usuario'
    )
    id_oferta_empresa = models.ForeignKey(
        'OfertaEmpresa',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_column='id_oferta_empresa'
    )
    
    fecha_guardado = models.DateTimeField(auto_now_add=True)
    nota_personal = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'guardar_trabajo'
        unique_together = [
            ['id_usuario', 'id_oferta_usuario'],
            ['id_usuario', 'id_oferta_empresa']
        ]
        indexes = [
            models.Index(fields=['id_usuario', '-fecha_guardado']),
        ]