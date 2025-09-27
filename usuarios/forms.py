# usuarios/forms.py
from django import forms
from usuarios.models import Usuario, Profile 
from usuarios.models import Departamento, Provincia, Distrito, Certificacion, Calificacion
from usuarios.widgets import MultiFileInput  


class RegisterEmpresaForm(forms.Form):
    ruc = forms.CharField(
        max_length=11,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingresa el RUC',
            'class': 'form-control',
            'maxlength': '11'
        })
    )
    
    razon_social = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'readonly': True,
            'placeholder': 'Se llenará automáticamente',
            'class': 'form-control'
        })
    )
    
    telefono = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingresa el teléfono',
            'class': 'form-control'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Ingresa el correo electrónico',
            'class': 'form-control'
        })
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Ingresa la contraseña',
            'class': 'form-control'
        })
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirma la contraseña',
            'class': 'form-control'
        })
    )

    def clean_ruc(self):
        ruc = self.cleaned_data.get('ruc')
        if ruc and len(ruc) != 11:
            raise forms.ValidationError('El RUC debe tener exactamente 11 dígitos.')
        if ruc and not ruc.isdigit():
            raise forms.ValidationError('El RUC debe contener solo números.')
        return ruc

class RegisterFormStep1(forms.Form):
    dni = forms.CharField(
        max_length=8,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingresa tu DNI',
            'class': 'form-control',
            'maxlength': '8'
        })
    )
    
    nombre = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'readonly': True,
            'placeholder': 'Se llenará automáticamente',
            'class': 'form-control'
        })
    )
    
    apellido = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'readonly': True,
            'placeholder': 'Se llenará automáticamente',
            'class': 'form-control'
        })
    )
    
    telefono = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ingresa tu teléfono',
            'class': 'form-control'
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Ingresa tu correo electrónico',
            'class': 'form-control'
        })
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Ingresa tu contraseña',
            'class': 'form-control'
        })
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirma tu contraseña',
            'class': 'form-control'
        })
    )


class RegisterFormStep2(forms.Form):
    direccion = forms.CharField(max_length=255, required=True)

    # Solo se usa el queryset en el servidor (para validación y guardado), no para mostrar opciones en HTML
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(), required=True, empty_label=None
    )
    provincia = forms.ModelChoiceField(
        queryset=Provincia.objects.all(), required=True, empty_label=None
    )
    distrito = forms.ModelChoiceField(
        queryset=Distrito.objects.all(), required=True, empty_label=None
    )


class RegisterFormStep3(forms.Form):
    habilidades = forms.CharField(
        widget=forms.Textarea(attrs={'required': True}),
        label="Habilidades y oficios *"
    )
    experiencia = forms.ChoiceField(
        choices=[
            ('', 'Selecciona tu experiencia'),
            ('1', '1 año'),
            ('1-3', '1-3 años'),
            ('3-5', '3-5 años'),
            ('5+', 'Más de 5 años')
        ],
        required=False
    )
    disponibilidad = forms.ChoiceField(
        choices=[
            ('', 'Selecciona tu disponibilidad'),
            ('mañanas', 'Solo mañanas'),
            ('tardes', 'Solo tardes'),
            ('todo_dia', 'Todo el día'),
        ],
        required=True
    )
    tarifa = forms.DecimalField(required=False, min_value=0, label="Tarifa por hora", initial=0)
    estudios = forms.ChoiceField(
        choices=[
            ('ninguno', 'No tengo estudios universitarios'),
            ('universitario', 'Universitario')
        ],
        required=True
    )
    carrera = forms.CharField(required=False, max_length=100, label="Carrera universitaria (si aplica)")
    certificaciones = forms.FileField(
        required=False,
        help_text="Puedes subir un archivo PDF o imagen de tus certificados"
    )

class MultipleCertificacionesForm(forms.Form):
    archivos = forms.FileField(
        widget=MultiFileInput(attrs={'multiple': True}),
        required=True,
        help_text="Puedes subir varios archivos (PDF, imágenes, etc.)"
    )
    descripcion = forms.CharField(
        max_length=255,
        required=False,
        help_text="Descripción opcional para todas las certificaciones"
    )

    
class RegisterFormStep4(forms.Form):
    antecedentes = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={
            'accept': '.pdf,.jpg,.jpeg,.png'
        }),
        help_text="Sube un archivo PDF o imagen"
    )


# Movido fuera de la clase para evitar errores de sintaxis
email = forms.EmailField(
    label="Correo electrónico",
    widget=forms.EmailInput(attrs={'placeholder': 'ejemplo@correo.com'}),
)


class CalificacionForm(forms.ModelForm):
    class Meta:
        model  = Calificacion
        fields = ['puntuacion', 'comentario']
        widgets = {
            'puntuacion': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comentario': forms.Textarea(attrs={'rows': 3})
        }