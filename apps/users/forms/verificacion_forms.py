"""
Forms de Verificación y Certificaciones
Responsabilidad: Validación de documentos de verificación
"""

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
            'fecha_expiracion',
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
                'placeholder': 'Descripción breve de la certificación...'
            }),
            'archivo': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,image/*'
            }),
            'fecha_obtencion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'fecha_expiracion': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
        }
        labels = {
            'titulo': 'Título de la certificación',
            'institucion': 'Institución emisora',
            'descripcion': 'Descripción',
            'archivo': 'Archivo de certificación',
            'fecha_obtencion': 'Fecha de obtención',
            'fecha_expiracion': 'Fecha de expiración (opcional)',
        }
    
    def clean_archivo(self):
        """Valida el archivo de certificación"""
        archivo = self.cleaned_data.get('archivo')
        
        if archivo:
            max_size = 5 * 1024 * 1024  # 5MB
            if archivo.size > max_size:
                raise forms.ValidationError('El archivo no debe superar los 5MB')
            
            allowed_types = [
                'application/pdf',
                'image/jpeg',
                'image/jpg',
                'image/png'
            ]
            if archivo.content_type not in allowed_types:
                raise forms.ValidationError('Solo se permiten archivos PDF o imágenes')
        
        return archivo
    
    def clean(self):
        """Valida que la fecha de expiración sea posterior a la de obtención"""
        cleaned_data = super().clean()
        fecha_obtencion = cleaned_data.get('fecha_obtencion')
        fecha_expiracion = cleaned_data.get('fecha_expiracion')
        
        if fecha_obtencion and fecha_expiracion:
            if fecha_expiracion < fecha_obtencion:
                raise forms.ValidationError(
                    'La fecha de expiración debe ser posterior a la fecha de obtención'
                )
        
        return cleaned_data


class VerificacionForm(forms.ModelForm):
    """
    Formulario para solicitar verificación de identidad
    """
    
    class Meta:
        model = Verificacion
        fields = [
            'tipo',
            'archivo_url',
            'archivo_frontal',
            'archivo_posterior',
            'observaciones',
        ]
        widgets = {
            'tipo': forms.Select(attrs={
                'class': 'form-control'
            }),
            'archivo_url': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': '.pdf,image/*'
            }),
            'archivo_frontal': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'archivo_posterior': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'observaciones': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Información adicional (opcional)...'
            }),
        }
        labels = {
            'tipo': 'Tipo de verificación',
            'archivo_url': 'Archivo principal',
            'archivo_frontal': 'Foto frontal del documento',
            'archivo_posterior': 'Foto posterior del documento',
            'observaciones': 'Observaciones',
        }
    
    def __init__(self, *args, **kwargs):
        """Personaliza el formulario según el tipo de verificación"""
        super().__init__(*args, **kwargs)
        
        # Hacer campos requeridos según el tipo
        tipo = self.data.get('tipo')
        
        if tipo == 'dni':
            self.fields['archivo_frontal'].required = True
            self.fields['archivo_posterior'].required = True
        elif tipo in ['antecedentes', 'telefono', 'email']:
            self.fields['archivo_url'].required = True
    
    def clean(self):
        """Valida que se suban los archivos necesarios según el tipo"""
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        
        if tipo == 'dni':
            if not cleaned_data.get('archivo_frontal'):
                self.add_error('archivo_frontal', 'Se requiere la foto frontal del DNI')
            if not cleaned_data.get('archivo_posterior'):
                self.add_error('archivo_posterior', 'Se requiere la foto posterior del DNI')
        
        elif tipo in ['antecedentes', 'telefono', 'email']:
            if not cleaned_data.get('archivo_url'):
                self.add_error('archivo_url', f'Se requiere el archivo para {tipo}')
        
        return cleaned_data


class MultipleCertificacionesForm(forms.Form):
    """
    Formulario para subir múltiples certificaciones a la vez
    """
    
    archivos = forms.FileField(
        widget=MultipleFileInput(attrs={
            'multiple': True,
            'class': 'form-control',
            'accept': '.pdf,image/*'
        }),
        required=True,
        help_text='Puedes subir varios archivos (PDF, imágenes, etc.)',
        label='Certificaciones'
    )
    
    descripcion = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Descripción general (opcional)'
        }),
        help_text='Descripción opcional para todas las certificaciones',
        label='Descripción'
    )
    
    def clean_archivos(self):
        """Valida múltiples archivos"""
        files = self.files.getlist('archivos')
        max_size = 5 * 1024 * 1024  # 5MB
        
        if not files:
            raise forms.ValidationError('Debes subir al menos un archivo')
        
        for file in files:
            if file.size > max_size:
                raise forms.ValidationError(
                    f'El archivo {file.name} excede el tamaño máximo de 5MB'
                )
            
            allowed_types = [
                'application/pdf',
                'image/jpeg',
                'image/jpg',
                'image/png'
            ]
            if file.content_type not in allowed_types:
                raise forms.ValidationError(
                    f'El archivo {file.name} no es un formato válido'
                )
        
        return files