"""
Forms del módulo Users
Divididos por responsabilidad siguiendo SRP
"""

from .auth_forms import (
    RegisterFormStep1,
    RegisterFormStep2,
    RegisterFormStep3,
    RegisterFormStep4,
    RegisterEmpresaForm
)
from .perfil_forms import (
    PerfilUpdateForm,
    TarifaForm
)
from .verificacion_forms import (
    CertificacionForm,
    VerificacionForm
)
from .calificacion_forms import CalificacionForm

__all__ = [
    # Auth
    'RegisterFormStep1',
    'RegisterFormStep2',
    'RegisterFormStep3',
    'RegisterFormStep4',
    'RegisterEmpresaForm',
    'VerificacionForm',
    'CertificacionForm',
]