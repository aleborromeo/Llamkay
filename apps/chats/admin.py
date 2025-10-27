# apps/chats/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Conversacion, Mensaje


@admin.register(Conversacion)
class ConversacionAdmin(admin.ModelAdmin):
    list_display = [
        'id_conversacion',
        'usuario_1_display',
        'usuario_2_display',
        'created_at',
        'activa',
        'bloqueada',
        'ultimo_mensaje_at'
    ]
    list_filter = ['created_at', 'activa', 'bloqueada']
    search_fields = [
        'id_usuario_1__nombres',
        'id_usuario_1__apellidos',
        'id_usuario_2__nombres',
        'id_usuario_2__apellidos'
    ]
    readonly_fields = ['created_at', 'updated_at', 'ultimo_mensaje_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('Información de la Conversación', {
            'fields': ('id_usuario_1', 'id_usuario_2', 'created_at', 'updated_at')
        }),
        ('Contexto', {
            'fields': ('id_oferta_usuario', 'id_oferta_empresa')
        }),
        ('Estado', {
            'fields': ('activa', 'bloqueada', 'ultimo_mensaje_at')
        }),
    )

    def usuario_1_display(self, obj):
        return f"{obj.id_usuario_1.nombres} {obj.id_usuario_1.apellidos}"
    usuario_1_display.short_description = 'Usuario 1'

    def usuario_2_display(self, obj):
        return f"{obj.id_usuario_2.nombres} {obj.id_usuario_2.apellidos}"
    usuario_2_display.short_description = 'Usuario 2'


@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = [
        'id_mensaje',
        'remitente_display',
        'conversacion_link',
        'contenido_corto',
        'created_at',  
        'leido',
        'eliminado',
        'tipo'
    ]
    list_filter = [
        'leido',
        'eliminado',
        'tipo',
        'created_at'
    ]
    search_fields = [
        'contenido',
        'id_remitente__nombres',
        'id_remitente__apellidos'
    ]
    readonly_fields = ['created_at', 'fecha_leido']
    date_hierarchy = 'created_at' 

    fieldsets = (
        ('Información del Mensaje', {
            'fields': ('id_conversacion', 'id_remitente', 'tipo', 'contenido', 'archivo')
        }),
        ('Estado', {
            'fields': ('leido', 'fecha_leido', 'eliminado', 'created_at')
        }),
    )

    def contenido_corto(self, obj):
        if obj.eliminado:
            return "[Mensaje eliminado]"
        if not obj.contenido:
            return f"[{obj.get_tipo_display()}]"
        return (obj.contenido[:50] + '...') if len(obj.contenido) > 50 else obj.contenido
    contenido_corto.short_description = 'Contenido'

    def remitente_display(self, obj):
        return f"{obj.id_remitente.nombres} {obj.id_remitente.apellidos}"
    remitente_display.short_description = 'Remitente'

    def conversacion_link(self, obj):
        url = f"/admin/chats/conversacion/{obj.id_conversacion.id_conversacion}/change/"
        return format_html('<a href="{}">Ver chat</a>', url)
    conversacion_link.short_description = 'Conversación'