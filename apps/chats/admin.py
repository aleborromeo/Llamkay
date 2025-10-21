from django.contrib import admin
from .models import Conversacion, Mensaje


@admin.register(Conversacion)
class ConversacionAdmin(admin.ModelAdmin):
    list_display = ['id_conversacion', 'id_usuario_1', 'id_usuario_2', 'created_at']
    list_filter = ['created_at', 'activa', 'bloqueada']
    search_fields = ['id_usuario_1__nombres', 'id_usuario_1__apellidos', 
                     'id_usuario_2__nombres', 'id_usuario_2__apellidos']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Información de la Conversación', {
            'fields': ('id_usuario_1', 'id_usuario_2', 'created_at', 'updated_at')
        }),
        ('Contexto', {
            'fields': ('id_oferta_usuario', 'id_oferta_empresa', 'id_contrato')
        }),
        ('Estado', {
            'fields': ('activa', 'bloqueada', 'id_bloqueada_por', 'ultimo_mensaje_at')
        }),
    )


@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ['id_mensaje', 'id_remitente', 'id_conversacion', 'contenido_corto', 
                    'fecha_envio', 'editado', 'eliminado', 'leido', 'tipo']
    list_filter = ['editado', 'eliminado', 'leido', 'tipo', 'fecha_envio']
    search_fields = ['contenido', 'id_remitente__nombres', 'id_remitente__apellidos']
    readonly_fields = ['fecha_envio', 'updated_at']
    date_hierarchy = 'fecha_envio'
    
    fieldsets = (
        ('Información del Mensaje', {
            'fields': ('id_conversacion', 'id_remitente', 'tipo', 'contenido', 'archivo')
        }),
        ('Estado', {
            'fields': ('editado', 'eliminado', 'leido', 'fecha_leido', 'fecha_envio', 'updated_at')
        }),
    )
    
    def contenido_corto(self, obj):
        """Muestra los primeros 50 caracteres del contenido"""
        if obj.eliminado:
            return "[Mensaje eliminado]"
        if not obj.contenido:
            return f"[{obj.get_tipo_display()}]"
        return obj.contenido[:50] + '...' if len(obj.contenido) > 50 else obj.contenido
    
    contenido_corto.short_description = 'Contenido'