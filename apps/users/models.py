from django.db import models
from django.contrib.auth.models import User


# Modelos completos del módulo de usuarios (versión extendida)
# Incluye: autenticación personalizada, antecedentes, perfil público,
# recordatorios, recomendaciones, historial de eventos, eliminación lógica y más.

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.utils import timezone


class Departamento(models.Model):
    id_departamento = models.IntegerField(primary_key=True)
    nombre = models.CharField(blank=True, null=True)

    class Meta:
        db_table = 'departamento'
    
    def __str__(self):
        return self.nombre
    
    
class Provincia(models.Model):
    id_provincia = models.IntegerField(primary_key=True)
    id_departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='id_departamento', blank=True, null=True)
    nombre = models.CharField(blank=True, null=True)

    class Meta:
        db_table = 'provincia'


class Distrito(models.Model):
    id_distrito = models.IntegerField(primary_key=True)
    id_provincia = models.ForeignKey('Provincia', models.DO_NOTHING, db_column='id_provincia', blank=True, null=True)
    nombre = models.CharField(blank=True, null=True)

    class Meta:
        db_table = 'distrito'
        

class Comunidad(models.Model):
    id_comunidad = models.IntegerField(primary_key=True)
    id_distrito = models.ForeignKey('Distrito', models.DO_NOTHING, db_column='id_distrito', blank=True, null=True)
    nombre = models.CharField(blank=True, null=True)

    class Meta:
        db_table = 'comunidad'


class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil') #para mantener la personalizacion
    
    id_usuario = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, blank=False, null=False)
    nombres = models.CharField(blank=True, null=True)
    apellidos = models.CharField(blank=True, null=True)
    dni = models.CharField(blank=True, null=True)
    telefono = models.CharField(blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    email = models.CharField(blank=True, null=True)
    clave = models.TextField(blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    tipo_usuario = models.TextField(blank=True, null=True)  # This field type is a guess.
    id_comunidad = models.ForeignKey(Comunidad, models.DO_NOTHING, db_column='id_comunidad', blank=True, null=True)
    habilitado = models.BooleanField(blank=True, null=True)
    
    genero = models.CharField(
        max_length=10,
        choices=[("masculino", "Masculino"), ("femenino", "Femenino"), ("otro", "Otro")],
        default="otro"
    )

    perfil_publico_activo = models.BooleanField(default=False, verbose_name="Perfil público activado")
    biografia_flexible = models.TextField(blank=True, null=True, verbose_name="Descripción libre del usuario")
    eliminado_en = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de eliminación lógica")

    def obtener_slug_publico(self):
        return slugify(f"{self.username}-{self.id}")

    def esta_eliminado(self):
        return self.eliminado_en is not None

    def eliminar_logicamente(self):
        self.eliminado_en = timezone.now()
        self.save()

    class Meta:
        db_table = 'usuario'


class PerfilPublico(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name="perfil_publico")
    slug = models.SlugField(unique=True)
    resumen = models.TextField(verbose_name="Resumen público")
    habilidades = models.JSONField(default=list, verbose_name="Lista de habilidades")
    mostrar_email = models.BooleanField(default=False)
    mostrar_telefono = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.usuario.obtener_slug_publico()
        super().save(*args, **kwargs)


class Recomendacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="recomendaciones")
    autor = models.CharField(max_length=255, verbose_name="Nombre del recomendante")
    comentario = models.TextField(verbose_name="Comentario")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de emisión")
    visible = models.BooleanField(default=True, verbose_name="¿Mostrar públicamente?")


class ConfiguracionRecordatorio(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    canal = models.CharField(
        max_length=10,
        choices=[
            ("push", "Notificación Push"),
            ("email", "Correo electrónico"),
            ("sms", "Mensaje de texto")
        ],
        default="push",
        verbose_name="Canal preferido"
    )
    anticipacion_horas = models.PositiveIntegerField(default=24, verbose_name="Horas de anticipación")
    habilitado = models.BooleanField(default=True, verbose_name="¿Recordatorios habilitados?")


class RegistroEvento(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="eventos")
    tipo_evento = models.CharField(max_length=100, verbose_name="Tipo de evento")
    fecha_hora = models.DateTimeField(verbose_name="Fecha y hora")
    canal = models.CharField(max_length=10, verbose_name="Canal utilizado")
    estado = models.CharField(max_length=20, default="enviado", verbose_name="Estado del evento")


class SolicitudEliminacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    tipo = models.CharField(
        max_length=20,
        choices=[
            ("cuenta", "Eliminar cuenta completa"),
            ("historial", "Eliminar solo historial")
        ],
        verbose_name="Tipo de solicitud"
    )
    fecha_solicitud = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de solicitud")
    confirmada = models.BooleanField(default=False, verbose_name="¿Confirmada por el usuario?")


class RegistroError(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True)
    modulo = models.CharField(max_length=50, verbose_name="Módulo")
    mensaje = models.TextField(verbose_name="Mensaje del error")
    nivel = models.CharField(
        max_length=10,
        choices=[("WARNING", "Advertencia"), ("ERROR", "Error")],
        default="ERROR",
        verbose_name="Nivel de severidad"
    )
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Fecha del evento")


class ActividadReciente(models.Model):
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField()
    fecha = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'actividad_reciente'


class Avisos(models.Model):
    id_aviso = models.IntegerField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    mensaje = models.CharField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'avisos'


class Calificacion(models.Model):
    id_usuario = models.ForeignKey(Usuario, related_name='calificaciones_recibidas', on_delete=models.CASCADE)
    autor = models.ForeignKey(Usuario, related_name='calificaciones_enviadas', on_delete=models.SET_NULL, null=True, blank=True)

    puntuacion = models.PositiveSmallIntegerField()
    comentario = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('id_usuario', 'autor')  # Evita duplicados por usuario que califica


class Categoriatrabajo(models.Model):
    id_categoria = models.IntegerField(primary_key=True)
    nombre = models.CharField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'categoriatrabajo'


class Denuncia(models.Model):
    id_denuncia = models.IntegerField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    id_empleador = models.ForeignKey('Empleador', models.DO_NOTHING, db_column='id_empleador', blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    estado = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        db_table = 'denuncia'


class Disponibilidad(models.Model):
    id_disponibilidad = models.IntegerField(primary_key=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'disponibilidad'
    

class Empleador(models.Model):
    id_empleador = models.IntegerField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    nombre_empresa = models.CharField(blank=True, null=True)
    ruc = models.CharField(blank=True, null=True)
    verificado = models.BooleanField(blank=True, null=True)

    class Meta:
        db_table = 'empleador'


class Filtrotrabajoporzona(models.Model):
    id_filtro = models.IntegerField(primary_key=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    id_comunidad = models.ForeignKey(Comunidad, models.DO_NOTHING, db_column='id_comunidad', blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'filtrotrabajoporzona'


class Habilidad(models.Model):
    id_habilidad = models.IntegerField(primary_key=True)
    nombre = models.CharField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'habilidad'


class Ofertatrabajo(models.Model):
    id_oferta = models.IntegerField(primary_key=True)
    id_empleador = models.ForeignKey(Empleador, models.DO_NOTHING, db_column='id_empleador', blank=True, null=True)
    id_categoria = models.ForeignKey(Categoriatrabajo, models.DO_NOTHING, db_column='id_categoria', blank=True, null=True)
    titulo = models.CharField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    sueldo = models.FloatField(blank=True, null=True)
    estado = models.BooleanField(blank=True, null=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)

    class Meta:
        db_table = 'ofertatrabajo'


class Politicalegal(models.Model):
    id_politica = models.IntegerField(primary_key=True)
    nombre = models.TextField(blank=True, null=True)
    descripcion = models.TextField(blank=True, null=True)
    fecha_actualizacion = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'politicalegal'


class Postulacion(models.Model):
    id_postulacion = models.IntegerField(primary_key=True)
    id_oferta = models.ForeignKey(Ofertatrabajo, models.DO_NOTHING, db_column='id_oferta', blank=True, null=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    estado = models.TextField(blank=True, null=True)
    fecha_postulacion = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'postulacion'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Relación con auth.User
    
    id_profile = models.AutoField(primary_key=True)
    id_usuario = models.OneToOneField('Usuario', models.DO_NOTHING, db_column='id_usuario')
    fecha_registro = models.DateTimeField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    foto_url = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)
    redes_sociales = models.JSONField(blank=True, null=True)
    id_comunidad = models.ForeignKey(Comunidad, models.DO_NOTHING, db_column='id_comunidad', blank=True, null=True)
    id_distrito = models.ForeignKey(Distrito, models.DO_NOTHING, db_column='id_distrito', blank=True, null=True)
    id_provincia = models.ForeignKey('Provincia', models.DO_NOTHING, db_column='id_provincia', blank=True, null=True)
    id_departamento = models.ForeignKey(Departamento, models.DO_NOTHING, db_column='id_departamento', blank=True, null=True)
    categorias = models.TextField(blank=True, null=True)
    habilidades = models.TextField(blank=True, null=True)
    ocupacion = models.CharField(max_length=100)
    experiencia = models.PositiveIntegerField(default=0, verbose_name="Años de experiencia")
    portafolio_url = models.URLField(blank=True, null=True)

    class Meta:
        db_table = 'profile'

        
class TrabajosRealizados(models.Model):
    usuario = models.ForeignKey('Usuario', models.DO_NOTHING)
    descripcion = models.TextField(blank=True, null=True)
    fecha_inicio = models.DateField(blank=True, null=True)
    fecha_fin = models.DateField(blank=True, null=True)
    empresa = models.CharField(max_length=255, blank=True, null=True)
    rol = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'trabajos_realizados'

class Certificacion(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='certificaciones/')
    descripcion = models.CharField(max_length=255)
    fecha_subida = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'certificacion'


class AntecedentePenal(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    archivo = models.FileField(upload_to='penales/')
    aprobado = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True)

    class Meta:
        db_table = 'antecedente_penal'


class Empresa(models.Model):
    id_empresa = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    ruc = models.CharField(max_length=11, unique=True)
    razon_social = models.CharField(max_length=255)
    direccion = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    representante = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    fecha_registro = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'empresa'


class UsuarioCategoria(models.Model):
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario')
    id_categoria = models.ForeignKey(Categoriatrabajo, models.DO_NOTHING, db_column='id_categoria')

    class Meta:
        db_table = 'usuario_categoria'
        unique_together = (('id_usuario', 'id_categoria'),)


class UsuarioHabilidad(models.Model):
    id = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario')
    id_habilidad = models.ForeignKey(Habilidad, models.DO_NOTHING, db_column='id_habilidad')

    class Meta:
        db_table = 'usuario_habilidad'
        unique_together = (('id_usuario', 'id_habilidad'),)



class Verificacion(models.Model):
    id_verificacion = models.IntegerField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    estado = models.TextField(blank=True, null=True)  # This field type is a guess.
    fecha = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'verificacion'