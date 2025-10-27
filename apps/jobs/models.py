"""
Modelos de Jobs - Simplificado
"""
from django.db import models


# ==================== OFERTAS ====================
class OfertaUsuario(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('pausada', 'Pausada'),
        ('cerrada', 'Cerrada'),
    ]

    MODALIDAD_PAGO_CHOICES = [
        ('por_hora', 'Por Hora'),
        ('por_dia', 'Por Día'),
        ('por_proyecto', 'Por Proyecto'),
    ]

    id = models.AutoField(primary_key=True)
    id_empleador = models.ForeignKey('users.Usuario', on_delete=models.CASCADE)
    id_categoria = models.ForeignKey('users.CategoriaTrabajo', on_delete=models.RESTRICT)
    
    # Descripción
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    modalidad_pago = models.CharField(max_length=20, choices=MODALIDAD_PAGO_CHOICES)
    pago = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    moneda = models.CharField(max_length=3, default='PEN')
    
    # Ubicación
    id_departamento = models.ForeignKey('users.Departamento', on_delete=models.SET_NULL, null=True, blank=True)
    id_provincia = models.ForeignKey('users.Provincia', on_delete=models.SET_NULL, null=True, blank=True)
    id_distrito = models.ForeignKey('users.Distrito', on_delete=models.SET_NULL, null=True, blank=True)
    direccion_detalle = models.TextField(null=True, blank=True)
    
    # Fechas
    fecha_inicio_estimada = models.DateField(null=True, blank=True)
    fecha_limite = models.DateField(null=True, blank=True)
    
    # Estado
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activa')
    urgente = models.BooleanField(default=False)
    vistas = models.IntegerField(default=0)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'oferta_usuario'
        ordering = ['-created_at']


class OfertaEmpresa(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('pausada', 'Pausada'),
        ('cerrada', 'Cerrada'),
    ]

    MODALIDAD_PAGO_CHOICES = [
        ('por_hora', 'Por Hora'),
        ('mensual', 'Mensual'),
    ]

    id = models.AutoField(primary_key=True)
    id_empleador = models.ForeignKey('users.Usuario', on_delete=models.CASCADE)
    id_categoria = models.ForeignKey('users.CategoriaTrabajo', on_delete=models.RESTRICT)
    
    # Descripción
    titulo_puesto = models.CharField(max_length=255)
    descripcion = models.TextField()
    modalidad_pago = models.CharField(max_length=20, choices=MODALIDAD_PAGO_CHOICES)
    pago = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    moneda = models.CharField(max_length=3, default='PEN')
    
    # Detalles
    experiencia_requerida = models.CharField(max_length=100, null=True, blank=True)
    vacantes = models.IntegerField(default=1)
    
    # Ubicación
    id_departamento = models.ForeignKey('users.Departamento', on_delete=models.SET_NULL, null=True, blank=True)
    id_provincia = models.ForeignKey('users.Provincia', on_delete=models.SET_NULL, null=True, blank=True)
    id_distrito = models.ForeignKey('users.Distrito', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Estado
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activa')
    vistas = models.IntegerField(default=0)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'oferta_empresa'
        ordering = ['-created_at']


# ==================== POSTULACIONES ====================
class Postulacion(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En Revisión'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]

    id_postulacion = models.AutoField(primary_key=True)
    id_trabajador = models.ForeignKey('users.Usuario', on_delete=models.CASCADE)
    id_oferta_usuario = models.ForeignKey(OfertaUsuario, on_delete=models.CASCADE, null=True, blank=True)
    id_oferta_empresa = models.ForeignKey(OfertaEmpresa, on_delete=models.CASCADE, null=True, blank=True)
    
    # Información
    mensaje = models.TextField(null=True, blank=True)
    pretension_salarial = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    disponibilidad_inmediata = models.BooleanField(default=False)
    
    # Estado
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    leida = models.BooleanField(default=False)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'postulacion'


# ==================== CONTRATOS ====================
class Contrato(models.Model):
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
    id_postulacion = models.ForeignKey(Postulacion, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Detalles
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(null=True, blank=True)
    precio_acordado = models.DecimalField(max_digits=10, decimal_places=2)
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


# ==================== PAGOS ====================
class Pago(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('fallido', 'Fallido'),
    ]

    id_pago = models.AutoField(primary_key=True)
    id_contrato = models.ForeignKey(Contrato, on_delete=models.RESTRICT)
    
    # Montos
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    monto_trabajador = models.DecimalField(max_digits=10, decimal_places=2)
    comision = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    moneda = models.CharField(max_length=3, default='PEN')
    
    # Estado
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pago'


# ==================== CALIFICACIONES ====================
class Calificacion(models.Model):
    id_calificacion = models.AutoField(primary_key=True)
    id_contrato = models.ForeignKey(Contrato, on_delete=models.CASCADE)
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
    puntuacion = models.IntegerField()  # 1-5
    comentario = models.TextField(null=True, blank=True)
    
    # Auditoría
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'calificacion'
        unique_together = [['id_contrato', 'id_autor']]


# ==================== TRABAJOS GUARDADOS ====================
class GuardarTrabajo(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey('users.Usuario', on_delete=models.CASCADE)
    id_oferta_usuario = models.ForeignKey(OfertaUsuario, on_delete=models.CASCADE, null=True, blank=True)
    id_oferta_empresa = models.ForeignKey(OfertaEmpresa, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'guardar_trabajo'