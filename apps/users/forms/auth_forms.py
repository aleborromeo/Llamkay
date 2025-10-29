from django import forms
from django.contrib.auth.models import User
from apps.users.models import Usuario, Departamento, Provincia, Distrito
from apps.users.widgets import MultipleFileInput 

class RegisterFormStep1(forms.Form):
    """Paso 1: Datos personales básicos"""
    # Identificación
    dni = forms.CharField(
        max_length=8,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '00000000',
            'maxlength': '8'
        })
    )
    nombre = forms.CharField(max_length=100, required=True)
    apellido = forms.CharField(max_length=100, required=True)
    
    # NUEVOS CAMPOS
    fecha_nacimiento = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'max': '2007-01-01'  # Mínimo 18 años
        })
    )
    genero = forms.ChoiceField(
        choices=Usuario.GENERO_CHOICES,
        required=True
    )
    
    # Contacto
    telefono = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    
    # Seguridad
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8
    )
    password2 = forms.CharField(widget=forms.PasswordInput)
    
    def clean_dni(self):
        dni = self.cleaned_data.get('dni')
        if not dni.isdigit():
            raise forms.ValidationError("El DNI debe contener solo números")
        if len(dni) != 8:
            raise forms.ValidationError("El DNI debe tener 8 dígitos")
        if Usuario.objects.filter(dni=dni).exists():
            raise forms.ValidationError("Este DNI ya está registrado")
        return dni
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está en uso")
        return email


class RegisterFormStep2(forms.Form):
    """Paso 2: Ubicación"""
    direccion = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: Av. Larco 123, Dpto. 501'
        })
    )
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        required=True
    )
    provincia = forms.ModelChoiceField(
        queryset=Provincia.objects.none(),
        required=True
    )
    distrito = forms.ModelChoiceField(
        queryset=Distrito.objects.none(),
        required=True
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'departamento' in self.data:
            try:
                departamento_id = int(self.data.get('departamento'))
                self.fields['provincia'].queryset = Provincia.objects.filter(
                    id_departamento=departamento_id
                ).order_by('nombre')
            except (ValueError, TypeError):
                pass
        
        if 'provincia' in self.data:
            try:
                provincia_id = int(self.data.get('provincia'))
                self.fields['distrito'].queryset = Distrito.objects.filter(
                    id_provincia=provincia_id
                ).order_by('nombre')
            except (ValueError, TypeError):
                pass


class RegisterFormStep3(forms.Form):
    """Paso 3: Perfil profesional - Solo trabajadores"""
    # Habilidades
    habilidades = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Describe tus habilidades y oficios...'
        }),
        required=True
    )
    
    # NUEVO: Ocupación principal
    ocupacion = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: Carpintero, Electricista, Plomero...'
        })
    )
    
    # Experiencia
    experiencia = forms.ChoiceField(
        choices=[
            ('', 'Selecciona tu experiencia'),
            ('sin_experiencia', 'Sin experiencia'),
            ('1', 'Menos de 1 año'),
            ('1-3', '1-3 años'),
            ('3-5', '3-5 años'),
            ('5+', 'Más de 5 años'),
        ],
        required=False
    )
    
    experiencia_anios = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Años de experiencia'
        })
    )
    
    # Disponibilidad
    disponibilidad = forms.ChoiceField(
        choices=[
            ('', 'Selecciona tu disponibilidad'),
            ('tiempo_completo', 'Tiempo completo'),
            ('medio_tiempo', 'Medio tiempo'),
            ('por_horas', 'Por horas'),
            ('fines_semana', 'Fines de semana'),
            ('flexible', 'Flexible'),
        ],
        required=True
    )
    
    # Educación
    estudios = forms.ChoiceField(
        choices=[
            ('', 'Selecciona tu nivel'),
            ('primaria', 'Primaria'),
            ('secundaria', 'Secundaria'),
            ('tecnico', 'Técnico'),
            ('universitario', 'Universitario'),
            ('posgrado', 'Posgrado'),
        ],
        required=True
    )
    
    carrera = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: Ingeniería Civil'
        })
    )
    
    certificaciones = forms.FileField(
        required=False,
        widget=MultipleFileInput(attrs={  
            'accept': '.pdf,image/*'
        })
    )


class RegisterFormStep4(forms.Form):
    """Paso 4: Antecedentes penales"""
    antecedentes = forms.FileField(
        required=True,
        widget=forms.FileInput(attrs={  
            'accept': '.pdf,.jpg,.jpeg,.png'
        })
    )
    
    def clean_antecedentes(self):
        file = self.cleaned_data.get('antecedentes')
        if file:
            # Validar tamaño (5MB)
            if file.size > 5 * 1024 * 1024:
                raise forms.ValidationError("El archivo no puede pesar más de 5MB")
            # Validar extensión
            ext = file.name.split('.')[-1].lower()
            if ext not in ['pdf', 'jpg', 'jpeg', 'png']:
                raise forms.ValidationError("Solo se permiten archivos PDF, JPG o PNG")
        return file


class RegisterEmpresaForm(forms.Form):
    """Paso 1 para empresas"""
    ruc = forms.CharField(
        max_length=11,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': '00000000000',
            'maxlength': '11'
        })
    )
    razon_social = forms.CharField(max_length=255, required=True)
    telefono = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, min_length=8)
    password2 = forms.CharField(widget=forms.PasswordInput)
    
    def clean_ruc(self):
        ruc = self.cleaned_data.get('ruc')
        if not ruc.isdigit():
            raise forms.ValidationError("El RUC debe contener solo números")
        if len(ruc) != 11:
            raise forms.ValidationError("El RUC debe tener 11 dígitos")
        return ruc
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo ya está en uso")
        return email