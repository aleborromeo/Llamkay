"""
Forms de Autenticación y Registro
Responsabilidad: Validación de datos de registro
"""

from django import forms
from apps.users.models import Departamento, Provincia, Distrito
from apps.users.widgets import MultipleFileInput


class RegisterEmpresaForm(forms.Form):
    """Formulario de registro para empresas"""
    
    ruc = forms.CharField(
        max_length=11,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingresa el RUC',
            'class': 'form-control',
            'maxlength': '11'
        }),
        label='RUC'
    )
    
    razon_social = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'readonly': True,
            'placeholder': 'Se llenará automáticamente',
            'class': 'form-control'
        }),
        label='Razón Social'
    )
    
    telefono = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingresa el teléfono',
            'class': 'form-control'
        }),
        label='Teléfono'
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Ingresa el correo electrónico',
            'class': 'form-control'
        }),
        label='Email'
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Ingresa la contraseña',
            'class': 'form-control'
        }),
        label='Contraseña'
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirma la contraseña',
            'class': 'form-control'
        }),
        label='Confirmar Contraseña'
    )

    def clean_ruc(self):
        """Valida el formato del RUC"""
        ruc = self.cleaned_data.get('ruc')
        if ruc and len(ruc) != 11:
            raise forms.ValidationError('El RUC debe tener exactamente 11 dígitos.')
        if ruc and not ruc.isdigit():
            raise forms.ValidationError('El RUC debe contener solo números.')
        return ruc
    
    def clean(self):
        """Valida que las contraseñas coincidan"""
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        
        return cleaned_data


class RegisterFormStep1(forms.Form):
    """Formulario Step 1: Datos personales básicos"""
    
    dni = forms.CharField(
        max_length=8,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingresa tu DNI',
            'class': 'form-control',
            'maxlength': '8'
        }),
        label='DNI'
    )
    
    nombre = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'readonly': True,
            'placeholder': 'Se llenará automáticamente',
            'class': 'form-control'
        }),
        label='Nombres'
    )
    
    apellido = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'readonly': True,
            'placeholder': 'Se llenará automáticamente',
            'class': 'form-control'
        }),
        label='Apellidos'
    )
    
    telefono = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingresa tu teléfono',
            'class': 'form-control'
        }),
        label='Teléfono'
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Ingresa tu correo electrónico',
            'class': 'form-control'
        }),
        label='Email'
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Ingresa tu contraseña',
            'class': 'form-control'
        }),
        label='Contraseña'
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirma tu contraseña',
            'class': 'form-control'
        }),
        label='Confirmar Contraseña'
    )
    
    def clean_dni(self):
        """Valida el formato del DNI"""
        dni = self.cleaned_data.get('dni')
        if dni and len(dni) != 8:
            raise forms.ValidationError('El DNI debe tener exactamente 8 dígitos.')
        if dni and not dni.isdigit():
            raise forms.ValidationError('El DNI debe contener solo números.')
        return dni


class RegisterFormStep2(forms.Form):
    """Formulario Step 2: Ubicación"""
    
    direccion = forms.CharField(
        max_length=255,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingresa tu dirección',
            'class': 'form-control'
        }),
        label='Dirección'
    )

    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        required=True,
        empty_label='Selecciona un departamento',
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Departamento'
    )
    
    provincia = forms.ModelChoiceField(
        queryset=Provincia.objects.all(),
        required=True,
        empty_label='Selecciona una provincia',
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Provincia'
    )
    
    distrito = forms.ModelChoiceField(
        queryset=Distrito.objects.all(),
        required=True,
        empty_label='Selecciona un distrito',
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Distrito'
    )


class RegisterFormStep3(forms.Form):
    """Formulario Step 3: Perfil Profesional"""
    
    habilidades = forms.CharField(
        widget=forms.Textarea(attrs={
            'required': True,
            'rows': 4,
            'placeholder': 'Describe tus habilidades y oficios principales...',
            'class': 'form-control'
        }),
        label='Habilidades y oficios'
    )
    
    experiencia = forms.ChoiceField(
        choices=[
            ('', 'Selecciona tu experiencia'),
            ('sin_experiencia', 'Sin experiencia'), 
            ('1', 'Menos de 1 año'),
            ('1-3', '1-3 años'),
            ('3-5', '3-5 años'),
            ('5+', 'Más de 5 años')
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Experiencia'
    )
    
    disponibilidad = forms.ChoiceField(
        choices=[
            ('', 'Selecciona tu disponibilidad'),
            ('tiempo_completo', 'Tiempo completo'),
            ('medio_tiempo', 'Medio tiempo'),        
            ('por_horas', 'Por horas'), 
            ('fines_semana', 'Fines de semana'),     
            ('flexible', 'Flexible'),                
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Disponibilidad'
    )
    
    tarifa = forms.DecimalField(
        required=False, 
        min_value=0, 
        max_digits=10,
        decimal_places=2,
        label='Tarifa por hora (opcional)', 
        initial=0,
        widget=forms.NumberInput(attrs={
            'placeholder': 'Ej: 15.50',
            'step': '0.01',
            'class': 'form-control'
        })
    )
    
    estudios = forms.ChoiceField(
        choices=[
            ('', 'Selecciona tu nivel de estudios'),
            ('primaria', 'Primaria'),      
            ('secundaria', 'Secundaria'),   
            ('tecnico', 'Técnico'),          
            ('universitario', 'Universitario'),
            ('posgrado', 'Posgrado')          
        ],
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Nivel de Estudios'
    )
    
    carrera = forms.CharField(
        required=False, 
        max_length=100, 
        label='Carrera universitaria (si aplica)',
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: Ingeniería Civil',
            'class': 'form-control'
        })
    )
    
    certificaciones = forms.FileField(
        required=False,
        widget=MultipleFileInput(attrs={
            'accept': '.pdf,image/*',
            'multiple': True,
            'class': 'form-control'
        }),
        help_text='Puedes subir varios archivos (PDF, JPG, PNG)',
        label='Certificaciones (opcional)'
    )
    
    def clean_certificaciones(self):
        """Valida los archivos de certificación"""
        files = self.files.getlist('certificaciones')
        max_size = 5 * 1024 * 1024  # 5MB
        
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


class RegisterFormStep4(forms.Form):
    """Formulario Step 4: Antecedentes penales"""
    
    antecedentes = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={
            'accept': '.pdf,.jpg,.jpeg,.png',
            'class': 'form-control'
        }),
        help_text='Sube un archivo PDF o imagen de tus antecedentes penales',
        label='Antecedentes Penales'
    )
    
    def clean_antecedentes(self):
        """Valida el archivo de antecedentes"""
        file = self.cleaned_data.get('antecedentes')
        
        if file:
            max_size = 5 * 1024 * 1024  # 5MB
            if file.size > max_size:
                raise forms.ValidationError('El archivo excede el tamaño máximo de 5MB')
            
            allowed_types = [
                'application/pdf',
                'image/jpeg',
                'image/jpg',
                'image/png'
            ]
            if file.content_type not in allowed_types:
                raise forms.ValidationError('Formato de archivo no válido')
        
        return file