from django.contrib import admin
from .models import (
    OfertaUsuario, OfertaEmpresa, Postulacion, Contrato,
    SesionTrabajo, Pago, Calificacion, GuardarTrabajo
)


@admin.register(OfertaUsuario)
class OfertaUsuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_empleador', 'titulo', 'estado', 'pago', 'fecha_publicacion', 'vistas', 'postulaciones_count']
    list_filter = ['estado', 'modalidad_pago', 'urgente', 'fecha_publicacion']
    search_fields = ['titulo', 'descripcion', 'id_empleador__nombres', 'id_empleador__apellidos']
    readonly_fields = ['fecha_publicacion', 'fecha_registro', 'updated_at', 'vistas', 'postulaciones_count']
    date_hierarchy = 'fecha_publicacion'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id_empleador', 'id_categoria', 'titulo', 'descripcion', 'estado')
        }),
        ('Pago', {
            'fields': ('modalidad_pago', 'pago', 'moneda')
        }),
        ('Ubicación', {
            'fields': ('id_departamento', 'id_provincia', 'id_distrito', 'id_comunidad', 
                      'direccion_detalle', 'latitud', 'longitud', 'radio_km')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio_estimada', 'fecha_limite', 'fecha_publicacion', 
                      'horas_limite', 'fecha_registro', 'updated_at')
        }),
        ('Detalles', {
            'fields': ('herramientas', 'urgente', 'foto', 'numero_contacto')
        }),
        ('Métricas', {
            'fields': ('vistas', 'postulaciones_count')
        }),
    )


@admin.register(OfertaEmpresa)
class OfertaEmpresaAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_empleador', 'titulo_puesto', 'estado', 'modalidad_trabajo', 
                    'vacantes', 'fecha_publicacion', 'vistas', 'postulaciones_count']
    list_filter = ['estado', 'modalidad_pago', 'modalidad_trabajo', 'fecha_publicacion']
    search_fields = ['titulo_puesto', 'descripcion', 'id_empleador__nombres', 'id_empleador__apellidos']
    readonly_fields = ['fecha_publicacion', 'fecha_registro', 'updated_at', 'vistas', 'postulaciones_count']
    date_hierarchy = 'fecha_publicacion'
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('id_empleador', 'id_categoria', 'titulo_puesto', 'descripcion', 'estado')
        }),
        ('Pago', {
            'fields': ('modalidad_pago', 'pago', 'moneda', 'rango_salarial')
        }),
        ('Detalles del Empleo', {
            'fields': ('modalidad_trabajo', 'experiencia_requerida', 'requisitos_calificaciones',
                      'beneficios_compensaciones', 'vacantes')
        }),
        ('Ubicación', {
            'fields': ('id_departamento', 'id_provincia', 'id_distrito', 'id_comunidad',
                      'direccion_detalle', 'latitud', 'longitud', 'radio_km')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio_estimada', 'fecha_limite', 'fecha_publicacion',
                      'fecha_registro', 'updated_at')
        }),
        ('Contacto', {
            'fields': ('foto', 'numero_contacto')
        }),
        ('Métricas', {
            'fields': ('vistas', 'postulaciones_count')
        }),
    )


@admin.register(Postulacion)
class PostulacionAdmin(admin.ModelAdmin):
    list_display = ['id_postulacion', 'id_trabajador', 'get_oferta', 'estado', 
                    'fecha_postulacion', 'leida']
    list_filter = ['estado', 'leida', 'disponibilidad_inmediata', 'fecha_postulacion']
    search_fields = ['id_trabajador__nombres', 'id_trabajador__apellidos', 'mensaje']
    readonly_fields = ['fecha_postulacion', 'updated_at']
    date_hierarchy = 'fecha_postulacion'
    
    fieldsets = (
        ('Información', {
            'fields': ('id_trabajador', 'id_oferta_usuario', 'id_oferta_empresa')
        }),
        ('Postulación', {
            'fields': ('mensaje', 'pretension_salarial', 'disponibilidad_inmediata', 'cv_adjunto')
        }),
        ('Estado', {
            'fields': ('estado', 'leida', 'fecha_leida', 'fecha_postulacion', 'updated_at')
        }),
    )
    
    def get_oferta(self, obj):
        if obj.id_oferta_usuario:
            return f"Usuario: {obj.id_oferta_usuario.titulo}"
        elif obj.id_oferta_empresa:
            return f"Empresa: {obj.id_oferta_empresa.titulo_puesto}"
        return "-"
    get_oferta.short_description = 'Oferta'


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = ['id_contrato', 'id_empleador', 'id_trabajador', 'titulo', 
                    'precio_acordado', 'estado', 'fecha_inicio', 'created_at']
    list_filter = ['estado', 'fecha_inicio', 'created_at']
    search_fields = ['titulo', 'id_empleador__nombres', 'id_trabajador__nombres']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Partes', {
            'fields': ('id_empleador', 'id_trabajador', 'id_postulacion', 
                      'id_oferta_usuario', 'id_oferta_empresa')
        }),
        ('Detalles del Contrato', {
            'fields': ('titulo', 'descripcion', 'precio_acordado', 'moneda', 'modalidad_pago')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin_estimada', 'fecha_fin_real', 
                      'created_at', 'updated_at')
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
    )


@admin.register(SesionTrabajo)
class SesionTrabajoAdmin(admin.ModelAdmin):
    list_display = ['id_sesion', 'id_contrato', 'fecha', 'hora_inicio', 
                    'hora_fin', 'horas_trabajadas', 'aprobada']
    list_filter = ['aprobada', 'fecha']
    search_fields = ['id_contrato__titulo', 'nota']
    readonly_fields = ['created_at']
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Contrato', {
            'fields': ('id_contrato',)
        }),
        ('Sesión', {
            'fields': ('fecha', 'hora_inicio', 'hora_fin', 'horas_trabajadas', 'nota')
        }),
        ('Aprobación', {
            'fields': ('aprobada', 'created_at')
        }),
    )


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['id_pago', 'id_contrato', 'monto_total', 'monto_trabajador',
                    'metodo_pago', 'estado', 'created_at']
    list_filter = ['estado', 'metodo_pago', 'created_at']
    search_fields = ['id_contrato__titulo', 'referencia_externa']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contrato', {
            'fields': ('id_contrato',)
        }),
        ('Montos', {
            'fields': ('monto_total', 'monto_trabajador', 'comision_plataforma', 'moneda')
        }),
        ('Método y Estado', {
            'fields': ('metodo_pago', 'estado')
        }),
        ('Referencias', {
            'fields': ('referencia_externa', 'comprobante')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'fecha_procesado')
        }),
    )


@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ['id_calificacion', 'id_autor', 'id_receptor', 'puntuacion',
                    'rol_autor', 'activa', 'fecha']
    list_filter = ['puntuacion', 'rol_autor', 'activa', 'editada', 'fecha']
    search_fields = ['id_autor__nombres', 'id_receptor__nombres', 'comentario']
    readonly_fields = ['fecha', 'updated_at']
    date_hierarchy = 'fecha'
    
    fieldsets = (
        ('Contrato y Partes', {
            'fields': ('id_contrato', 'id_autor', 'id_receptor', 'rol_autor')
        }),
        ('Calificación', {
            'fields': ('puntuacion', 'comentario')
        }),
        ('Detalles', {
            'fields': ('puntualidad', 'calidad_trabajo', 'comunicacion')
        }),
        ('Estado', {
            'fields': ('activa', 'editada', 'fecha', 'updated_at')
        }),
    )


@admin.register(GuardarTrabajo)
class GuardarTrabajoAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_usuario', 'get_trabajo', 'fecha_guardado']
    list_filter = ['fecha_guardado']
    search_fields = ['id_usuario__nombres', 'id_usuario__apellidos', 'nota_personal']
    readonly_fields = ['fecha_guardado']
    date_hierarchy = 'fecha_guardado'
    
    fieldsets = (
        ('Usuario y Trabajo', {
            'fields': ('id_usuario', 'id_oferta_usuario', 'id_oferta_empresa')
        }),
        ('Detalles', {
            'fields': ('nota_personal', 'fecha_guardado')
        }),
    )
    
    def get_trabajo(self, obj):
        if obj.id_oferta_usuario:
            return f"Usuario: {obj.id_oferta_usuario.titulo}"
        elif obj.id_oferta_empresa:
            return f"Empresa: {obj.id_oferta_empresa.titulo_puesto}"
        return "-"
    get_trabajo.short_description = 'Trabajo'