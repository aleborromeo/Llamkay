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
            'puntualidad',
            'calidad_trabajo',
            'comunicacion',
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
            'puntualidad': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'class': 'form-control'
            }),
            'calidad_trabajo': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'class': 'form-control'
            }),
            'comunicacion': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
                'class': 'form-control'
            }),
        }
        labels = {
            'puntuacion': 'Calificación general (1-5 estrellas)',
            'comentario': 'Comentario',
            'puntualidad': 'Puntualidad (1-5)',
            'calidad_trabajo': 'Calidad del trabajo (1-5)',
            'comunicacion': 'Comunicación (1-5)',
        }
        help_texts = {
            'puntuacion': 'Calificación obligatoria de 1 a 5 estrellas',
            'comentario': 'Comparte tu experiencia de trabajo',
            'puntualidad': 'Opcional: Califica la puntualidad',
            'calidad_trabajo': 'Opcional: Califica la calidad del trabajo',
            'comunicacion': 'Opcional: Califica la comunicación',
        }
    
    def clean_puntuacion(self):
        """Valida que la puntuación esté en el rango correcto"""
        puntuacion = self.cleaned_data.get('puntuacion')
        
        if puntuacion is None:
            raise forms.ValidationError('La puntuación es obligatoria')
        
        if not (1 <= puntuacion <= 5):
            raise forms.ValidationError('La puntuación debe estar entre 1 y 5')
        
        return puntuacion
    
    def clean_puntualidad(self):
        """Valida puntualidad si se proporciona"""
        puntualidad = self.cleaned_data.get('puntualidad')
        
        if puntualidad is not None and not (1 <= puntualidad <= 5):
            raise forms.ValidationError('La puntualidad debe estar entre 1 y 5')
        
        return puntualidad
    
    def clean_calidad_trabajo(self):
        """Valida calidad del trabajo si se proporciona"""
        calidad = self.cleaned_data.get('calidad_trabajo')
        
        if calidad is not None and not (1 <= calidad <= 5):
            raise forms.ValidationError('La calidad debe estar entre 1 y 5')
        
        return calidad
    
    def clean_comunicacion(self):
        """Valida comunicación si se proporciona"""
        comunicacion = self.cleaned_data.get('comunicacion')
        
        if comunicacion is not None and not (1 <= comunicacion <= 5):
            raise forms.ValidationError('La comunicación debe estar entre 1 y 5')
        
        return comunicacion
    
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
    Para casos donde no se necesitan detalles adicionales
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