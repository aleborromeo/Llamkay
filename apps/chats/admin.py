from django.contrib import admin
from .models import Chat, Mensaje


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ['id_chat', 'usuario_1', 'usuario_2', 'fecha_creacion']
    list_filter = ['fecha_creacion']
    search_fields = ['usuario_1__nombres', 'usuario_1__apellidos', 
                     'usuario_2__nombres', 'usuario_2__apellidos']
    readonly_fields = ['fecha_creacion']
    date_hierarchy = 'fecha_creacion'
    
    fieldsets = (
        ('Información del Chat', {
            'fields': ('usuario_1', 'usuario_2', 'fecha_creacion')
        }),
    )


@admin.register(Mensaje)
class MensajeAdmin(admin.ModelAdmin):
    list_display = ['id_mensaje', 'remitente', 'id_chat', 'contenido_corto', 
                    'fecha_envio', 'editado', 'eliminado', 'leido']
    list_filter = ['editado', 'eliminado', 'leido', 'fecha_envio']
    search_fields = ['contenido', 'remitente__nombres', 'remitente__apellidos']
    readonly_fields = ['fecha_envio']
    date_hierarchy = 'fecha_envio'
    
    fieldsets = (
        ('Información del Mensaje', {
            'fields': ('id_chat', 'remitente', 'contenido')
        }),
        ('Estado', {
            'fields': ('editado', 'eliminado', 'leido', 'fecha_envio')
        }),
    )
    
    def contenido_corto(self, obj):
        """Muestra los primeros 50 caracteres del contenido"""
        if obj.eliminado:
            return "[Mensaje eliminado]"
        return obj.contenido[:50] + '...' if len(obj.contenido) > 50 else obj.contenido
    
    contenido_corto.short_description = 'Contenido'