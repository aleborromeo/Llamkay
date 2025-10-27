# soporte/admin.py
from django.contrib import admin
from .models import Denuncia, Notificacion


# ==================== DENUNCIAS ====================
@admin.register(Denuncia)
class DenunciaAdmin(admin.ModelAdmin):
    """Admin para Denuncias"""
    list_display = [
        'id_denuncia',
        'id_reportante',
        'id_denunciado',
        'motivo',
        'estado',
        'created_at',
    ]
    list_filter = ['estado', 'motivo', 'created_at']
    search_fields = [
        'id_reportante__nombres',
        'id_reportante__apellidos',
        'id_denunciado__nombres',
        'id_denunciado__apellidos',
        'descripcion'
    ]
    readonly_fields = ['created_at', 'fecha_resolucion']
    date_hierarchy = 'created_at'
    list_per_page = 25

    fieldsets = (
        ('Información Básica', {
            'fields': ('id_reportante', 'id_denunciado', 'motivo', 'descripcion')
        }),
        ('Estado y Resolución', {
            'fields': ('estado', 'resolucion')
        }),
        ('Auditoría', {
            'fields': ('created_at', 'fecha_resolucion'),
            'classes': ('collapse',)
        }),
    )

    def has_delete_permission(self, request, obj=None):
        """Solo superusuarios pueden eliminar denuncias"""
        return request.user.is_superuser


# ==================== NOTIFICACIONES ====================
@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    """Admin para Notificaciones"""
    list_display = [
        'id_notificacion',
        'id_usuario',
        'tipo',
        'titulo',
        'leida',
        'created_at',
    ]
    list_filter = ['tipo', 'leida', 'created_at']
    search_fields = [
        'id_usuario__nombres',
        'id_usuario__apellidos',
        'titulo',
        'mensaje',
    ]
    readonly_fields = ['created_at', 'fecha_leida']
    date_hierarchy = 'created_at'
    list_per_page = 50

    fieldsets = (
        ('Información Básica', {
            'fields': ('id_usuario', 'tipo', 'titulo', 'mensaje', 'url')
        }),
        ('Estado', {
            'fields': ('leida', 'fecha_leida', 'created_at')
        }),
    )

    actions = ['marcar_como_leidas', 'marcar_como_no_leidas']

    def marcar_como_leidas(self, request, queryset):
        """Marcar notificaciones seleccionadas como leídas"""
        from django.utils import timezone
        count = queryset.update(leida=True, fecha_leida=timezone.now())
        self.message_user(request, f"{count} notificaciones marcadas como leídas.")
    marcar_como_leidas.short_description = "Marcar como leídas"

    def marcar_como_no_leidas(self, request, queryset):
        """Marcar notificaciones seleccionadas como no leídas"""
        count = queryset.update(leida=False, fecha_leida=None)
        self.message_user(request, f"{count} notificaciones marcadas como no leídas.")
    marcar_como_no_leidas.short_description = "Marcar como no leídas"