"""
Formularios del módulo Jobs
"""
from django import forms
from django.core.exceptions import ValidationError
from decimal import Decimal
from datetime import date

from .models import OfertaUsuario, OfertaEmpresa
from apps.users.models import Provincia, Distrito


class OfertaUsuarioForm(forms.ModelForm):
    """
    Formulario para crear/editar ofertas de trabajo de usuarios individuales
    """
    class Meta:
        model = OfertaUsuario
        fields = [
            'id_categoria',
            'titulo',
            'descripcion',
            'modalidad_pago',
            'pago',
            'id_departamento',
            'id_provincia',
            'id_distrito',
            'direccion_detalle',
            'fecha_inicio_estimada',
            'fecha_limite',
            'urgente',
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Jardinero por un día',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe el trabajo en detalle...',
                'required': True
            }),
            'id_categoria': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'modalidad_pago': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'pago': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01'
            }),
            'id_departamento': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'id_provincia': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'id_distrito': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'direccion_detalle': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Dirección específica del trabajo'
            }),
            'fecha_inicio_estimada': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'fecha_limite': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'urgente': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'id_categoria': 'Categoría',
            'titulo': 'Título del trabajo',
            'descripcion': 'Descripción',
            'modalidad_pago': 'Modalidad de pago',
            'pago': 'Monto a pagar (S/)',
            'id_departamento': 'Departamento',
            'id_provincia': 'Provincia',
            'id_distrito': 'Distrito',
            'direccion_detalle': 'Dirección detallada',
            'fecha_inicio_estimada': 'Fecha estimada de inicio',
            'fecha_limite': 'Fecha límite para postular',
            'urgente': '¿Es urgente?',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Inicializar querysets vacíos para ubicación
        self.fields['id_provincia'].queryset = Provincia.objects.none()
        self.fields['id_distrito'].queryset = Distrito.objects.none()

        # Si hay datos en POST, cargar las opciones correspondientes
        if 'id_departamento' in self.data:
            try:
                departamento_id = int(self.data.get('id_departamento'))
                self.fields['id_provincia'].queryset = Provincia.objects.filter(
                    id_departamento=departamento_id
                ).order_by('nombre')
            except (ValueError, TypeError):
                pass

        if 'id_provincia' in self.data:
            try:
                provincia_id = int(self.data.get('id_provincia'))
                self.fields['id_distrito'].queryset = Distrito.objects.filter(
                    id_provincia=provincia_id
                ).order_by('nombre')
            except (ValueError, TypeError):
                pass
        
        # Si estamos editando, cargar las opciones basadas en la instancia
        elif self.instance.pk:
            if self.instance.id_departamento:
                self.fields['id_provincia'].queryset = Provincia.objects.filter(
                    id_departamento=self.instance.id_departamento
                ).order_by('nombre')
            if self.instance.id_provincia:
                self.fields['id_distrito'].queryset = Distrito.objects.filter(
                    id_provincia=self.instance.id_provincia
                ).order_by('nombre')

    def clean_pago(self):
        """Validar que el pago sea positivo"""
        pago = self.cleaned_data.get('pago')
        if pago is not None and pago <= 0:
            raise ValidationError('El monto debe ser mayor a 0')
        return pago

    def clean_fecha_limite(self):
        """Validar que la fecha límite sea futura"""
        fecha_limite = self.cleaned_data.get('fecha_limite')
        if fecha_limite and fecha_limite < date.today():
            raise ValidationError('La fecha límite debe ser futura')
        return fecha_limite

    def clean(self):
        """Validaciones adicionales"""
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio_estimada')
        fecha_limite = cleaned_data.get('fecha_limite')

        if fecha_inicio and fecha_limite and fecha_inicio < fecha_limite:
            raise ValidationError(
                'La fecha de inicio debe ser posterior a la fecha límite de postulación'
            )

        return cleaned_data


class OfertaEmpresaForm(forms.ModelForm):
    """
    Formulario para crear/editar ofertas de trabajo de empresas
    """
    class Meta:
        model = OfertaEmpresa
        fields = [
            'id_categoria',
            'titulo_puesto',
            'descripcion',
            'modalidad_pago',
            'pago',
            'experiencia_requerida',
            'vacantes',
            'id_departamento',
            'id_provincia',
            'id_distrito',
        ]
        widgets = {
            'titulo_puesto': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: Desarrollador Full Stack',
                'required': True
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Descripción del puesto...',
                'required': True
            }),
            'id_categoria': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'modalidad_pago': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'pago': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0.01'
            }),
            'experiencia_requerida': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 2 años'
            }),
            'vacantes': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '1',
                'min': '1',
                'required': True
            }),
            'id_departamento': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'id_provincia': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'id_distrito': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
        }
        labels = {
            'id_categoria': 'Categoría',
            'titulo_puesto': 'Título del puesto',
            'descripcion': 'Descripción del puesto',
            'modalidad_pago': 'Modalidad de pago',
            'pago': 'Salario (S/)',
            'experiencia_requerida': 'Experiencia requerida',
            'vacantes': 'Número de vacantes',
            'id_departamento': 'Departamento',
            'id_provincia': 'Provincia',
            'id_distrito': 'Distrito',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Inicializar querysets vacíos
        self.fields['id_provincia'].queryset = Provincia.objects.none()
        self.fields['id_distrito'].queryset = Distrito.objects.none()

        # Cargar opciones según datos POST
        if 'id_departamento' in self.data:
            try:
                departamento_id = int(self.data.get('id_departamento'))
                self.fields['id_provincia'].queryset = Provincia.objects.filter(
                    id_departamento=departamento_id
                ).order_by('nombre')
            except (ValueError, TypeError):
                pass

        if 'id_provincia' in self.data:
            try:
                provincia_id = int(self.data.get('id_provincia'))
                self.fields['id_distrito'].queryset = Distrito.objects.filter(
                    id_provincia=provincia_id
                ).order_by('nombre')
            except (ValueError, TypeError):
                pass
        
        # Si estamos editando
        elif self.instance.pk:
            if self.instance.id_departamento:
                self.fields['id_provincia'].queryset = Provincia.objects.filter(
                    id_departamento=self.instance.id_departamento
                ).order_by('nombre')
            if self.instance.id_provincia:
                self.fields['id_distrito'].queryset = Distrito.objects.filter(
                    id_provincia=self.instance.id_provincia
                ).order_by('nombre')

    def clean_pago(self):
        """Validar que el pago sea positivo"""
        pago = self.cleaned_data.get('pago')
        if pago is not None and pago <= 0:
            raise ValidationError('El salario debe ser mayor a 0')
        return pago

    def clean_vacantes(self):
        """Validar que las vacantes sean positivas"""
        vacantes = self.cleaned_data.get('vacantes')
        if vacantes is not None and vacantes < 1:
            raise ValidationError('Debe haber al menos 1 vacante')
        return vacantes