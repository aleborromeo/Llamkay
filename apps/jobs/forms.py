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
        # ✅ Campos basados en el modelo actual
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
            'fecha_limite': forms.DateInput(
                attrs={'type': 'date', 'class': 'form-control'}
            ),
            'fecha_inicio_estimada': forms.DateInput(
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
            'direccion_detalle': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Dirección específica...'}
            ),
            'id_categoria': forms.Select(attrs={'class': 'form-control'}),
            'id_departamento': forms.Select(attrs={'class': 'form-control'}),
            'id_provincia': forms.Select(attrs={'class': 'form-control'}),
            'id_distrito': forms.Select(attrs={'class': 'form-control'}),
            'modalidad_pago': forms.Select(attrs={'class': 'form-control'}),
            'urgente': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Importar aquí para evitar circular imports
        from apps.users.models import Provincia, Distrito

        # Inicializar querysets vacíos para ubicación
        self.fields['id_provincia'].queryset = Provincia.objects.none()
        self.fields['id_distrito'].queryset = Distrito.objects.none()

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


class OfertaEmpresaForm(forms.ModelForm):
    """
    Formulario para crear/editar ofertas de trabajo de empresas
    """
    class Meta:
        model = OfertaEmpresa
        # ✅ Campos basados en el modelo actual
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
            'titulo_puesto': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: Desarrollador Full Stack'}
            ),
            'pago': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': '0.00', 'step': '0.01'}
            ),
            'experiencia_requerida': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Ej: 2 años'}
            ),
            'descripcion': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del puesto...'}
            ),
            'vacantes': forms.NumberInput(
                attrs={'class': 'form-control', 'placeholder': '1', 'min': '1'}
            ),
            'id_categoria': forms.Select(attrs={'class': 'form-control'}),
            'id_departamento': forms.Select(attrs={'class': 'form-control'}),
            'id_provincia': forms.Select(attrs={'class': 'form-control'}),
            'id_distrito': forms.Select(attrs={'class': 'form-control'}),
            'modalidad_pago': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Importar aquí para evitar circular imports
        from apps.users.models import Provincia, Distrito

        # Inicializar querysets vacíos
        self.fields['id_provincia'].queryset = Provincia.objects.none()
        self.fields['id_distrito'].queryset = Distrito.objects.none()

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