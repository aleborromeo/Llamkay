from django import forms
from apps.users.models import Profile, Departamento, Provincia, Distrito


class PerfilUpdateForm(forms.ModelForm):
    """
    Formulario para actualizar el perfil del usuario
    """
    
    class Meta:
        model = Profile
        fields = [
            'bio',
            'ocupacion',
            'experiencia_anios',
            'tarifa_hora',
            'foto_url',         
            'portafolio_url',
            'id_departamento',
            'id_provincia',
            'id_distrito',
            'perfil_publico',    
            'mostrar_email',
            'mostrar_telefono',
        ]
        widgets = {
            'bio': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Cuéntanos sobre ti...'
            }),
            'ocupacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tu ocupación principal'
            }),
            'experiencia_anios': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 0,
                'max': 50
            }),
            'tarifa_hora': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0
            }),
            'foto_url': forms.URLInput(attrs={  
                'class': 'form-control',
                'placeholder': 'https://ejemplo.com/foto.jpg'
            }),
            'portafolio_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://...'
            }),
            'id_departamento': forms.Select(attrs={'class': 'form-control'}),
            'id_provincia': forms.Select(attrs={'class': 'form-control'}),
            'id_distrito': forms.Select(attrs={'class': 'form-control'}),
            'perfil_publico': forms.CheckboxInput(attrs={ 
                'class': 'form-check-input'
            }),
            'mostrar_email': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'mostrar_telefono': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'bio': 'Biografía',
            'ocupacion': 'Ocupación',
            'experiencia_anios': 'Años de experiencia',
            'tarifa_hora': 'Tarifa por hora (S/)',
            'foto_url': 'URL de la foto de perfil',
            'portafolio_url': 'URL del portafolio',
            'id_departamento': 'Departamento',
            'id_provincia': 'Provincia',
            'id_distrito': 'Distrito',
            'perfil_publico': 'Perfil público',  
            'mostrar_email': 'Mostrar email públicamente',
            'mostrar_telefono': 'Mostrar teléfono públicamente',
        }
    
    def clean_tarifa_hora(self):
        """Valida que la tarifa sea positiva"""
        tarifa = self.cleaned_data.get('tarifa_hora')
        if tarifa is not None and tarifa < 0:
            raise forms.ValidationError('La tarifa debe ser un valor positivo')
        return tarifa
    
    def clean_experiencia_anios(self):
        """Valida que los años de experiencia sean razonables"""
        experiencia = self.cleaned_data.get('experiencia_anios')
        if experiencia is not None and (experiencia < 0 or experiencia > 50):
            raise forms.ValidationError('Los años de experiencia deben estar entre 0 y 50')
        return experiencia
    
    def clean_foto_url(self):
        """Valida que la URL de la foto sea válida (opcional)"""
        url = self.cleaned_data.get('foto_url')
        if url and not url.startswith(('http://', 'https://')):
            raise forms.ValidationError('La URL debe comenzar con http:// o https://')
        return url


class TarifaForm(forms.Form):
    """
    Formulario simple para actualizar solo la tarifa
    """
    
    tarifa_hora = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'step': '0.01',
            'placeholder': 'Ej: 25.00'
        }),
        label='Tarifa por hora (S/)'
    )
    
    def clean_tarifa_hora(self):
        """Valida que la tarifa sea razonable"""
        tarifa = self.cleaned_data.get('tarifa_hora')
        if tarifa and tarifa > 10000:
            raise forms.ValidationError('La tarifa parece demasiado alta. Verifica el valor.')
        return tarifa