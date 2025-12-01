"""
Forms de Calificación
Responsabilidad: Validación de calificaciones
"""

from django import forms
from apps.jobs.models import Calificacion


class CalificacionForm(forms.ModelForm):
    """
    Formulario para crear/editar calificaciones
    """
    
    class Meta:
        model = Calificacion
        fields = [
            'puntuacion',
            'comentario',
        ]
        widgets = {
            'puntuacion': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'class': 'form-control',
                'required': True
            }),
            'comentario': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Escribe tu opinión sobre el trabajo realizado...'
            }),
        }
        labels = {
            'puntuacion': 'Calificación general (1-5 estrellas)',
            'comentario': 'Comentario',
        }
        help_texts = {
            'puntuacion': 'Calificación obligatoria de 1 a 5 estrellas',
            'comentario': 'Comparte tu experiencia de trabajo',
        }
    
    def clean_puntuacion(self):
        """Valida que la puntuación esté en el rango correcto"""
        puntuacion = self.cleaned_data.get('puntuacion')
        
        if puntuacion is None:
            raise forms.ValidationError('La puntuación es obligatoria')
        
        if not (1 <= puntuacion <= 5):
            raise forms.ValidationError('La puntuación debe estar entre 1 y 5')
        
        return puntuacion
    
    def clean_comentario(self):
        """Valida que el comentario no sea muy corto ni muy largo"""
        comentario = self.cleaned_data.get('comentario', '').strip()
        
        if comentario and len(comentario) < 10:
            raise forms.ValidationError('El comentario debe tener al menos 10 caracteres')
        
        if comentario and len(comentario) > 1000:
            raise forms.ValidationError('El comentario no debe superar los 1000 caracteres')
        
        return comentario


class CalificacionSimpleForm(forms.Form):
    """
    Formulario simple de calificación (solo puntuación y comentario)
    """
    
    puntuacion = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={
            'min': 1,
            'max': 5,
            'class': 'form-control',
            'required': True
        }),
        label='Calificación (1-5 estrellas)'
    )
    
    comentario = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'rows': 3,
            'class': 'form-control',
            'placeholder': 'Comentario opcional...'
        }),
        label='Comentario'
    )
    
    def clean_puntuacion(self):
        """Valida la puntuación"""
        puntuacion = self.cleaned_data.get('puntuacion')
        if not (1 <= puntuacion <= 5):
            raise forms.ValidationError('La puntuación debe estar entre 1 y 5')
        return puntuacion