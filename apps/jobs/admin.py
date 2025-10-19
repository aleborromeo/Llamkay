from django.contrib import admin
from .models import OfertaUsuario, OfertaEmpresa, GuardarTrabajo


@admin.register(OfertaUsuario)
class OfertaUsuarioAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'empleador', 'pago', 'fecha_limite', 'estado', 'fecha_registro']
    list_filter = ['estado', 'fecha_registro', 'id_departamento']
    search_fields = ['titulo', 'descripcion', 'empleador__email']
    readonly_fields = ['fecha_registro']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('empleador', 'titulo', 'descripcion', 'herramientas')
        }),
        ('Detalles económicos y tiempo', {
            'fields': ('pago', 'horas_limite', 'fecha_limite')
        }),
        ('Ubicación', {
            'fields': ('id_departamento', 'id_provincia', 'id_distrito', 'id_comunidad', 'direccion_detalle')
        }),
        ('Contacto', {
            'fields': ('numero_contacto',)
        }),
        ('Multimedia', {
            'fields': ('foto',)
        }),
        ('Estado', {
            'fields': ('estado', 'fecha_registro')
        }),
    )


@admin.register(OfertaEmpresa)
class OfertaEmpresaAdmin(admin.ModelAdmin):
    list_display = ['titulo_puesto', 'empleador', 'rango_salarial', 'fecha_limite', 'estado', 'numero_postulantes']
    list_filter = ['estado', 'modalidad_trabajo', 'fecha_registro', 'id_departamento']
    search_fields = ['titulo_puesto', 'descripcion_puesto', 'empleador__email']
    readonly_fields = ['fecha_registro', 'numero_postulantes']
    
    fieldsets = (
        ('Información básica', {
            'fields': ('empleador', 'titulo_puesto', 'descripcion_puesto')
        }),
        ('Requisitos y condiciones', {
            'fields': ('rango_salarial', 'experiencia_requerida', 'modalidad_trabajo', 
                      'requisitos_calificaciones', 'beneficios_compensaciones')
        }),
        ('Fechas', {
            'fields': ('fecha_limite', 'fecha_registro')
        }),
        ('Ubicación', {
            'fields': ('id_departamento', 'id_provincia', 'id_distrito', 'id_comunidad', 'direccion_detalle')
        }),
        ('Contacto', {
            'fields': ('numero_contacto',)
        }),
        ('Multimedia y estadísticas', {
            'fields': ('foto', 'numero_postulantes')
        }),
        ('Estado', {
            'fields': ('estado',)
        }),
    )


@admin.register(GuardarTrabajo)
class GuardarTrabajoAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'content_type', 'object_id', 'fecha_guardado']
    list_filter = ['content_type', 'fecha_guardado']
    search_fields = ['usuario__email']
    readonly_fields = ['fecha_guardado']