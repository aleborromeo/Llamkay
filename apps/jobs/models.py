from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey


class OfertaUsuario(models.Model):
    """
    Modelo para ofertas de trabajo publicadas por usuarios individuales
    (tipo_usuario: 'ofrecer-trabajo' o 'ambos')
    """
    empleador = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        limit_choices_to={'tipo_usuario__in': ['ofrecer-trabajo', 'ambos']},
        related_name='ofertas_usuario',
        verbose_name='Empleador'
    )
    titulo = models.CharField(max_length=255, verbose_name='Título')
    pago = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Pago')
    horas_limite = models.TimeField(verbose_name='Hora límite')
    descripcion = models.TextField(verbose_name='Descripción')
    herramientas = models.TextField(verbose_name='Herramientas necesarias')
    foto = models.ImageField(upload_to='ofertas/', blank=True, null=True, verbose_name='Foto')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    fecha_limite = models.DateField(verbose_name='Fecha límite')
    
    # Ubicación
    id_departamento = models.ForeignKey(
        'users.Departamento', 
        models.DO_NOTHING, 
        null=True, 
        blank=True,
        verbose_name='Departamento'
    )
    id_provincia = models.ForeignKey(
        'users.Provincia', 
        models.DO_NOTHING, 
        null=True, 
        blank=True,
        verbose_name='Provincia'
    )
    id_distrito = models.ForeignKey(
        'users.Distrito', 
        models.DO_NOTHING, 
        null=True, 
        blank=True,
        verbose_name='Distrito'
    )
    id_comunidad = models.ForeignKey(
        'users.Comunidad', 
        models.DO_NOTHING, 
        null=True, 
        blank=True,
        verbose_name='Comunidad'
    )
    direccion_detalle = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Dirección detallada'
    )
    
    numero_contacto = models.CharField(
        max_length=15, 
        blank=False, 
        null=False,
        help_text="Número de WhatsApp para contacto (obligatorio)",
        verbose_name='Número de contacto'
    )
    
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('vencida', 'Vencida'),
        ('completada', 'Completada'),
    ]
    estado = models.CharField(
        max_length=10, 
        choices=ESTADO_CHOICES, 
        default='activa',
        verbose_name='Estado'
    )

    class Meta:
        verbose_name = 'Oferta de Usuario'
        verbose_name_plural = 'Ofertas de Usuarios'
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['-fecha_registro']),
            models.Index(fields=['estado']),
        ]

    def __str__(self):
        return f"{self.titulo} - {self.empleador.email}"


class OfertaEmpresa(models.Model):
    """
    Modelo para ofertas de trabajo publicadas por empresas
    (tipo_usuario: 'empresa')
    """
    empleador = models.ForeignKey(
        'users.Usuario',
        on_delete=models.CASCADE,
        limit_choices_to={'tipo_usuario': 'empresa'},
        related_name='ofertas_empresa',
        verbose_name='Empresa empleadora'
    )
    titulo_puesto = models.CharField(max_length=255, verbose_name='Título del puesto')
    rango_salarial = models.CharField(max_length=100, verbose_name='Rango salarial')
    experiencia_requerida = models.CharField(max_length=100, verbose_name='Experiencia requerida')
    modalidad_trabajo = models.CharField(
        max_length=100,
        verbose_name='Modalidad de trabajo',
        help_text='Remoto/Presencial/Híbrido'
    )
    descripcion_puesto = models.TextField(verbose_name='Descripción del puesto')
    requisitos_calificaciones = models.TextField(verbose_name='Requisitos y calificaciones')
    beneficios_compensaciones = models.TextField(verbose_name='Beneficios y compensaciones')
    numero_postulantes = models.PositiveIntegerField(default=0, verbose_name='Número de postulantes')
    foto = models.ImageField(upload_to='ofertas/', blank=True, null=True, verbose_name='Foto')
    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')
    fecha_limite = models.DateField(verbose_name='Fecha límite')
    
    # Ubicación
    id_departamento = models.ForeignKey(
        'users.Departamento', 
        models.DO_NOTHING, 
        null=True, 
        blank=True,
        verbose_name='Departamento'
    )
    id_provincia = models.ForeignKey(
        'users.Provincia', 
        models.DO_NOTHING, 
        null=True, 
        blank=True,
        verbose_name='Provincia'
    )
    id_distrito = models.ForeignKey(
        'users.Distrito', 
        models.DO_NOTHING, 
        null=True, 
        blank=True,
        verbose_name='Distrito'
    )
    id_comunidad = models.ForeignKey(
        'users.Comunidad', 
        models.DO_NOTHING, 
        null=True, 
        blank=True,
        verbose_name='Comunidad'
    )
    direccion_detalle = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Dirección detallada'
    )
    
    numero_contacto = models.CharField(
        max_length=15, 
        blank=False, 
        null=False,
        help_text="Número de WhatsApp para contacto (obligatorio)",
        verbose_name='Número de contacto'
    )
    
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('vencida', 'Vencida'),
        ('completada', 'Completada'),
    ]
    estado = models.CharField(
        max_length=10, 
        choices=ESTADO_CHOICES, 
        default='activa',
        verbose_name='Estado'
    )

    class Meta:
        verbose_name = 'Oferta de Empresa'
        verbose_name_plural = 'Ofertas de Empresas'
        ordering = ['-fecha_registro']
        indexes = [
            models.Index(fields=['-fecha_registro']),
            models.Index(fields=['estado']),
        ]

    def __str__(self):
        return f"{self.titulo_puesto} - {self.empleador.email}"


class GuardarTrabajo(models.Model):
    """
    Modelo para gestionar los trabajos guardados por los usuarios
    Utiliza GenericForeignKey para referenciar tanto OfertaUsuario como OfertaEmpresa
    """
    usuario = models.ForeignKey(
        'users.Usuario', 
        on_delete=models.CASCADE,
        related_name='trabajos_guardados',
        verbose_name='Usuario'
    )
    
    # Campos para referencia genérica
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    oferta = GenericForeignKey('content_type', 'object_id')
    
    fecha_guardado = models.DateTimeField(auto_now_add=True, verbose_name='Fecha guardado')

    class Meta:
        unique_together = ('usuario', 'content_type', 'object_id')
        verbose_name = 'Trabajo guardado'
        verbose_name_plural = 'Trabajos guardados'
        ordering = ['-fecha_guardado']
        indexes = [
            models.Index(fields=['usuario', 'content_type', 'object_id']),
        ]

    def __str__(self):
        return f"{self.usuario.email} guardó {self.oferta}"