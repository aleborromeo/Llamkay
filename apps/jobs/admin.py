# apps/jobs/admin.py
from django.contrib import admin
from .models import (
    OfertaUsuario, OfertaEmpresa, Postulacion, Contrato,
    Pago, Calificacion, GuardarTrabajo
)


@admin.register(OfertaUsuario)
class OfertaUsuarioAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_empleador', 'titulo', 'estado', 'pago', 'created_at', 'vistas']
    list_filter = ['estado', 'modalidad_pago', 'urgente', 'created_at']
    search_fields = ['titulo', 'descripcion', 'id_empleador__nombres', 'id_empleador__apellidos']
    readonly_fields = ['created_at', 'updated_at', 'vistas']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Información Básica', {
            'fields': ('id_empleador', 'id_categoria', 'titulo', 'descripcion', 'estado')
        }),
        ('Pago', {
            'fields': ('modalidad_pago', 'pago', 'moneda')
        }),
        ('Ubicación', {
            'fields': ('id_departamento', 'id_provincia', 'id_distrito', 'direccion_detalle')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio_estimada', 'fecha_limite')
        }),
        ('Detalles', {
            'fields': ('urgente',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'vistas')
        }),
    )


@admin.register(OfertaEmpresa)
class OfertaEmpresaAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_empleador', 'titulo_puesto', 'estado', 'pago', 'vacantes', 'created_at', 'vistas']
    list_filter = ['estado', 'modalidad_pago', 'created_at']
    search_fields = ['titulo_puesto', 'descripcion', 'id_empleador__nombres', 'id_empleador__apellidos']
    readonly_fields = ['created_at', 'updated_at', 'vistas']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Información Básica', {
            'fields': ('id_empleador', 'id_categoria', 'titulo_puesto', 'descripcion', 'estado')
        }),
        ('Pago', {
            'fields': ('modalidad_pago', 'pago', 'moneda')
        }),
        ('Detalles del Empleo', {
            'fields': ('experiencia_requerida', 'vacantes')
        }),
        ('Ubicación', {
            'fields': ('id_departamento', 'id_provincia', 'id_distrito')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at', 'vistas')
        }),
    )


@admin.register(Postulacion)
class PostulacionAdmin(admin.ModelAdmin):
    list_display = ['id_postulacion', 'id_trabajador', 'get_oferta', 'estado', 'created_at', 'leida']
    list_filter = ['estado', 'leida', 'disponibilidad_inmediata', 'created_at']
    search_fields = ['id_trabajador__nombres', 'id_trabajador__apellidos', 'mensaje']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Información', {
            'fields': ('id_trabajador', 'id_oferta_usuario', 'id_oferta_empresa')
        }),
        ('Postulación', {
            'fields': ('mensaje', 'pretension_salarial', 'disponibilidad_inmediata')
        }),
        ('Estado', {
            'fields': ('estado', 'leida')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at')
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
            'fields': ('id_empleador', 'id_trabajador', 'id_postulacion')
        }),
        ('Detalles del Contrato', {
            'fields': ('titulo', 'descripcion', 'precio_acordado', 'moneda')
        }),
        ('Fechas', {
            'fields': ('fecha_inicio', 'fecha_fin_estimada', 'fecha_fin_real')
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['id_pago', 'id_contrato', 'monto_total', 'monto_trabajador',
                    'comision', 'estado', 'created_at']
    list_filter = ['estado', 'created_at']
    search_fields = ['id_contrato__titulo']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Contrato', {
            'fields': ('id_contrato',)
        }),
        ('Montos', {
            'fields': ('monto_total', 'monto_trabajador', 'comision', 'moneda')
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
        ('Auditoría', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ['id_calificacion', 'id_contrato', 'id_autor', 'id_receptor', 'puntuacion', 'created_at']
    list_filter = ['puntuacion', 'created_at']
    search_fields = ['id_autor__nombres', 'id_receptor__nombres', 'comentario']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Contrato y Partes', {
            'fields': ('id_contrato', 'id_autor', 'id_receptor')
        }),
        ('Calificación', {
            'fields': ('puntuacion', 'comentario')
        }),
        ('Auditoría', {
            'fields': ('created_at',)
        }),
    )


@admin.register(GuardarTrabajo)
class GuardarTrabajoAdmin(admin.ModelAdmin):
    list_display = ['id', 'id_usuario', 'get_trabajo', 'created_at']
    list_filter = ['created_at']
    search_fields = ['id_usuario__nombres', 'id_usuario__apellidos']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Usuario y Trabajo', {
            'fields': ('id_usuario', 'id_oferta_usuario', 'id_oferta_empresa')
        }),
        ('Auditoría', {
            'fields': ('created_at',)
        }),
    )

    def get_trabajo(self, obj):
        if obj.id_oferta_usuario:
            return f"Usuario: {obj.id_oferta_usuario.titulo}"
        elif obj.id_oferta_empresa:
            return f"Empresa: {obj.id_oferta_empresa.titulo_puesto}"
        return "-"
    get_trabajo.short_description = 'Trabajo'