# apps/users/forms/verificacion_forms.py
from django import forms
from apps.users.models import Certificacion, Verificacion
from apps.users.widgets import MultipleFileInput


class CertificacionForm(forms.ModelForm):
    """
    Formulario para subir certificaciones
    """
    
    class Meta:
        model = Certificacion
        fields = [
            'titulo',
            'institucion',
            'descripcion',
            'archivo',
            'fecha_obtencion',
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Certificado en Electricidad'
            }),
            'institucion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: SENATI'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descripción breve...'
            }),
            'archivo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,image/*'
            }),
            'fecha_obtencion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        labels = {
            'titulo': 'Título',
            'institucion': 'Institución',
            'descripcion': 'Descripción',
            'archivo': 'Archivo',
            'fecha_obtencion': 'Fecha de obtención',
        }
    
    def clean_archivo(self):
        archivo = self.cleaned_data.get('archivo')
        if archivo:
            max_size = 5 * 1024 * 1024  # 5MB
            if archivo.size > max_size:
                raise forms.ValidationError('El archivo no debe superar los 5MB')
            allowed = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png']
            if archivo.content_type not in allowed:
                raise forms.ValidationError('Solo PDF o imágenes')
        return archivo


class VerificacionForm(forms.ModelForm):
    """
    Formulario para solicitar verificación de identidad
    """
    
    class Meta:
        model = Verificacion
        fields = [
            'tipo',
            'archivo_url',
            'observaciones',
        ]
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'archivo_url': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,image/*'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Información adicional...'
            }),
        }
        labels = {
            'tipo': 'Tipo de verificación',
            'archivo_url': 'Archivo de verificación',
            'observaciones': 'Observaciones',
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        archivo = cleaned_data.get('archivo_url')

        if tipo in ['dni', 'antecedentes', 'telefono', 'email'] and not archivo:
            self.add_error('archivo_url', 'Este campo es obligatorio para este tipo de verificación.')

        return cleaned_data


class MultipleCertificacionesForm(forms.Form):
    """
    Subir múltiples certificaciones
    """
    archivos = forms.FileField(
        widget=MultipleFileInput(attrs={
            'multiple': True,
            'class': 'form-control',
            'accept': '.pdf,image/*'
        }),
        required=True,
        label='Certificaciones',
        help_text='Puedes subir varios archivos'
    )
    
    descripcion = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Descripción general (opcional)'
        }),
        label='Descripción'
    )
    
    def clean_archivos(self):
        files = self.files.getlist('archivos')
        if not files:
            raise forms.ValidationError('Debes subir al menos un archivo')
        
        max_size = 5 * 1024 * 1024
        allowed = ['application/pdf', 'image/jpeg', 'image/jpg', 'image/png']
        
        for file in files:
            if file.size > max_size:
                raise forms.ValidationError(f'{file.name} excede 5MB')
            if file.content_type not in allowed:
                raise forms.ValidationError(f'{file.name} no es PDF o imagen')
        
        return files