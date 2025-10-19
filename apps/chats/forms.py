from django import forms
from .models import Mensaje


class MensajeForm(forms.ModelForm):
    """Formulario para crear un nuevo mensaje"""
    
    class Meta:
        model = Mensaje
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Escribe un mensaje...',
                'required': True,
                'id': 'mensaje-input'
            })
        }
        labels = {
            'contenido': ''
        }

    def clean_contenido(self):
        """Valida que el contenido no esté vacío"""
        contenido = self.cleaned_data.get('contenido', '').strip()
        if not contenido:
            raise forms.ValidationError('El mensaje no puede estar vacío.')
        return contenido


class EditarMensajeForm(forms.ModelForm):
    """Formulario para editar un mensaje existente"""
    
    class Meta:
        model = Mensaje
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'required': True,
                'id': 'editar-mensaje-input'
            })
        }
        labels = {
            'contenido': 'Editar mensaje'
        }

    def clean_contenido(self):
        """Valida que el contenido no esté vacío"""
        contenido = self.cleaned_data.get('contenido', '').strip()
        if not contenido:
            raise forms.ValidationError('El mensaje no puede estar vacío.')
        return contenido