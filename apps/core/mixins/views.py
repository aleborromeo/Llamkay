from django.contrib import messages
from django.shortcuts import redirect


class FormMessageMixin:
    """Mensajes automáticos en formularios"""
    success_message = "Operación exitosa"
    error_message = "Ocurrió un error"

    def form_valid(self, form):
        if self.success_message:
            messages.success(self.request, self.success_message)
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.error_message:
            messages.error(self.request, self.error_message)
        return super().form_invalid(form)
