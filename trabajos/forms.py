from django import forms
from django.core.exceptions import ValidationError
import re
from .models import OfertaUsuario, OfertaEmpresa
from usuarios.models import Provincia, Distrito, Comunidad

class OfertaUsuarioForm(forms.ModelForm):
    class Meta:
        model = OfertaUsuario
        exclude = ['empleador', 'estado', 'fecha_registro']
        widgets = {
            'horas_limite': forms.TimeInput(format='%H:%M:%S', attrs={'type': 'time'}),
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}),
            'numero_contacto': forms.TextInput(attrs={
                'placeholder': '+51999123456',
                'pattern': r'^\+?[1-9]\d{8,14}$',
                'title': 'Formato: +51999123456 (8 a 15 dígitos)',
                'required': True
            }),
        }

    def clean_numero_contacto(self):
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

        self.fields['id_provincia'].queryset = Provincia.objects.none()
        self.fields['id_distrito'].queryset = Distrito.objects.none()
        self.fields['id_comunidad'].queryset = Comunidad.objects.none()

        if 'id_departamento' in self.data:
            try:
                departamento_id = int(self.data.get('id_departamento'))
                self.fields['id_provincia'].queryset = Provincia.objects.filter(id_departamento=departamento_id)
            except (ValueError, TypeError):
                pass

        if 'id_provincia' in self.data:
            try:
                provincia_id = int(self.data.get('id_provincia'))
                self.fields['id_distrito'].queryset = Distrito.objects.filter(id_provincia=provincia_id)
            except (ValueError, TypeError):
                pass

        if 'id_distrito' in self.data:
            try:
                distrito_id = int(self.data.get('id_distrito'))
                self.fields['id_comunidad'].queryset = Comunidad.objects.filter(id_distrito=distrito_id)
            except (ValueError, TypeError):
                pass


class OfertaEmpresaForm(forms.ModelForm):
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
        ]
        widgets = {
            'fecha_limite': forms.DateInput(attrs={'type': 'date'}),
            'descripcion_puesto': forms.Textarea(attrs={'rows': 3}),
            'requisitos_calificaciones': forms.Textarea(attrs={'rows': 3}),
            'beneficios_compensaciones': forms.Textarea(attrs={'rows': 3}),
            'direccion_detalle': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['id_provincia'].queryset = Provincia.objects.none()
        self.fields['id_distrito'].queryset = Distrito.objects.none()
        self.fields['id_comunidad'].queryset = Comunidad.objects.none()

        if 'id_departamento' in self.data:
            try:
                departamento_id = int(self.data.get('id_departamento'))
                self.fields['id_provincia'].queryset = Provincia.objects.filter(id_departamento=departamento_id)
            except (ValueError, TypeError):
                pass

        if 'id_provincia' in self.data:
            try:
                provincia_id = int(self.data.get('id_provincia'))
                self.fields['id_distrito'].queryset = Distrito.objects.filter(id_provincia=provincia_id)
            except (ValueError, TypeError):
                pass

        if 'id_distrito' in self.data:
            try:
                distrito_id = int(self.data.get('id_distrito'))
                self.fields['id_comunidad'].queryset = Comunidad.objects.filter(id_distrito=distrito_id)
            except (ValueError, TypeError):
                pass
