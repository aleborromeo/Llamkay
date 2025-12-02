from django import forms
from django.core.exceptions import ValidationError
from decimal import Decimal

from apps.jobs.models import OfertaEmpresa
from apps.users.models import Provincia, Distrito


class OfertaEmpresaForm(forms.ModelForm):
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
        
        self.fields['id_provincia'].queryset = Provincia.objects.none()
        self.fields['id_distrito'].queryset = Distrito.objects.none()

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
        pago = self.cleaned_data.get('pago')
        if pago is not None and pago <= 0:
            raise ValidationError('El salario debe ser mayor a 0')
        return pago

    def clean_vacantes(self):
        vacantes = self.cleaned_data.get('vacantes')
        if vacantes is not None and vacantes < 1:
            raise ValidationError('Debe haber al menos 1 vacante')
        return vacantes