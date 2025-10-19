from django import forms
from django.core.exceptions import ValidationError
import re
from .models import OfertaUsuario, OfertaEmpresa


class OfertaUsuarioForm(forms.ModelForm):
    """
    Formulario para crear/editar ofertas de trabajo de usuarios individuales
    """
    class Meta:
        model = OfertaUsuario
        exclude = ['empleador', 'estado', 'fecha_registro']
        widgets = {
            'horas_limite': forms.TimeInput(
                format='%H:%M:%S', 
                attrs={'type': 'time', 'class': 'form-control'}
            ),
            'fecha_limite': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'titulo': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: Jardinero por un día'}
            ),
            'pago': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}
            ),
            'descripcion': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe el trabajo...'}
            ),
            'herramientas': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Herramientas necesarias...'}
            ),
            'direccion_detalle': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Dirección específica...'}
            ),
            'numero_contacto': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '+51999123456',
                    'pattern': r'^\+?[1-9]\d{8,14}$',
                    'title': 'Formato: +51999123456 (8 a 15 dígitos)',
                    'required': True
                }
            ),
            'id_departamento': forms.Select(attrs={'class': 'form-control'}),
            'id_provincia': forms.Select(attrs={'class': 'form-control'}),
            'id_distrito': forms.Select(attrs={'class': 'form-control'}),
            'id_comunidad': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_numero_contacto(self):
        """Valida y formatea el número de WhatsApp"""
        numero = self.cleaned_data.get('numero_contacto')
        if not numero:
            raise ValidationError("El número de WhatsApp es obligatorio.")
        
        # Limpiar espacios y caracteres especiales excepto +
        numero_limpio = re.sub(r'[^\d+]', '', numero)
        
        # Validar formato básico
        if not re.match(r'^\+?[1-9]\d{8,14}$', numero_limpio):
            raise ValidationError("Formato inválido. Use: +51999123456 (8 a 15 dígitos)")
        
        # Asegurar que tenga el prefijo +
        if not numero_limpio.startswith('+'):
            numero_limpio = '+' + numero_limpio
            
        return numero_limpio

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Importar aquí para evitar circular imports
        from apps.users.models import Provincia, Distrito, Comunidad

        # Inicializar querysets vacíos para ubicación
        self.fields['id_provincia'].queryset = Provincia.objects.none()
        self.fields['id_distrito'].queryset = Distrito.objects.none()
        self.fields['id_comunidad'].queryset = Comunidad.objects.none()

        # Si hay datos en POST, cargar las opciones correspondientes
        if 'id_departamento' in self.data:
            try:
                departamento_id = int(self.data.get('id_departamento'))
                self.fields['id_provincia'].queryset = Provincia.objects.filter(
                    id_departamento=departamento_id
                )
            except (ValueError, TypeError):
                pass

        if 'id_provincia' in self.data:
            try:
                provincia_id = int(self.data.get('id_provincia'))
                self.fields['id_distrito'].queryset = Distrito.objects.filter(
                    id_provincia=provincia_id
                )
            except (ValueError, TypeError):
                pass

        if 'id_distrito' in self.data:
            try:
                distrito_id = int(self.data.get('id_distrito'))
                self.fields['id_comunidad'].queryset = Comunidad.objects.filter(
                    id_distrito=distrito_id
                )
            except (ValueError, TypeError):
                pass
        
        # Si estamos editando, cargar las opciones basadas en la instancia
        elif self.instance.pk:
            if self.instance.id_departamento:
                self.fields['id_provincia'].queryset = Provincia.objects.filter(
                    id_departamento=self.instance.id_departamento
                )
            if self.instance.id_provincia:
                self.fields['id_distrito'].queryset = Distrito.objects.filter(
                    id_provincia=self.instance.id_provincia
                )
            if self.instance.id_distrito:
                self.fields['id_comunidad'].queryset = Comunidad.objects.filter(
                    id_distrito=self.instance.id_distrito
                )


class OfertaEmpresaForm(forms.ModelForm):
    """
    Formulario para crear/editar ofertas de trabajo de empresas
    """
    class Meta:
        model = OfertaEmpresa
        fields = [
            'titulo_puesto',
            'rango_salarial',
            'experiencia_requerida',
            'modalidad_trabajo',
            'descripcion_puesto',
            'requisitos_calificaciones',
            'beneficios_compensaciones',
            'numero_postulantes',
            'foto',
            'fecha_limite',
            'id_departamento',
            'id_provincia',
            'id_distrito',
            'id_comunidad',
            'direccion_detalle',
            'numero_contacto',
        ]
        widgets = {
            'fecha_limite': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'titulo_puesto': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: Desarrollador Full Stack'}
            ),
            'rango_salarial': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: S/2000 - S/3000'}
            ),
            'experiencia_requerida': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: 2 años'}
            ),
            'modalidad_trabajo': forms.Select(
                choices=[
                    ('', 'Seleccione...'),
                    ('remoto', 'Remoto'),
                    ('presencial', 'Presencial'),
                    ('hibrido', 'Híbrido'),
                ],
                attrs={'class': 'form-control'}
            ),
            'descripcion_puesto': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del puesto...'}
            ),
            'requisitos_calificaciones': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Requisitos...'}
            ),
            'beneficios_compensaciones': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Beneficios...'}
            ),
            'numero_postulantes': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': '0'}
            ),
            'direccion_detalle': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Dirección específica...'}
            ),
            'numero_contacto': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '+51999123456',
                    'pattern': r'^\+?[1-9]\d{8,14}$',
                    'title': 'Formato: +51999123456 (8 a 15 dígitos)',
                }
            ),
            'id_departamento': forms.Select(attrs={'class': 'form-control'}),
            'id_provincia': forms.Select(attrs={'class': 'form-control'}),
            'id_distrito': forms.Select(attrs={'class': 'form-control'}),
            'id_comunidad': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Importar aquí para evitar circular imports
        from apps.users.models import Provincia, Distrito, Comunidad

        # Inicializar querysets vacíos
        self.fields['id_provincia'].queryset = Provincia.objects.none()
        self.fields['id_distrito'].queryset = Distrito.objects.none()
        self.fields['id_comunidad'].queryset = Comunidad.objects.none()

        # Cargar opciones según datos POST
        if 'id_departamento' in self.data:
            try:
                departamento_id = int(self.data.get('id_departamento'))
                self.fields['id_provincia'].queryset = Provincia.objects.filter(
                    id_departamento=departamento_id
                )
            except (ValueError, TypeError):
                pass

        if 'id_provincia' in self.data:
            try:
                provincia_id = int(self.data.get('id_provincia'))
                self.fields['id_distrito'].queryset = Distrito.objects.filter(
                    id_provincia=provincia_id
                )
            except (ValueError, TypeError):
                pass

        if 'id_distrito' in self.data:
            try:
                distrito_id = int(self.data.get('id_distrito'))
                self.fields['id_comunidad'].queryset = Comunidad.objects.filter(
                    id_distrito=distrito_id
                )
            except (ValueError, TypeError):
                pass
        
        # Si estamos editando, cargar las opciones basadas en la instancia
        elif self.instance.pk:
            if self.instance.id_departamento:
                self.fields['id_provincia'].queryset = Provincia.objects.filter(
                    id_departamento=self.instance.id_departamento
                )
            if self.instance.id_provincia:
                self.fields['id_distrito'].queryset = Distrito.objects.filter(
                    id_provincia=self.instance.id_provincia
                )
            if self.instance.id_distrito:
                self.fields['id_comunidad'].queryset = Comunidad.objects.filter(
                    id_distrito=self.instance.id_distrito
                )