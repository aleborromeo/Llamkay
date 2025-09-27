from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario


def rol_requerido(roles_permitidos):
    """
    Decorador que verifica si el usuario tiene uno de los roles permitidos.
    
    Uso:
    @rol_requerido(['trabajador', 'empleador'])
    def mi_vista(request):
        # código de la vista
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            try:
                usuario = Usuario.objects.get(user=request.user)
                
                # Verificar si el tipo de usuario está en los roles permitidos
                if usuario.tipo_usuario in roles_permitidos:
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(request, f'No tienes permisos para acceder a esta sección. Se requiere rol: {", ".join(roles_permitidos)}')
                    return redirect('usuarios:dashboard')
                    
            except Usuario.DoesNotExist:
                messages.error(request, 'Tu perfil de usuario no está configurado correctamente.')
                return redirect('usuarios:dashboard')
                
        return _wrapped_view
    return decorator


def solo_trabajadores(view_func):
    """Decorador específico para vistas que solo pueden ver trabajadores"""
    return rol_requerido(['trabajador', 'trabajador_empleador'])(view_func)


def solo_empleadores(view_func):
    """Decorador específico para vistas que solo pueden ver empleadores"""
    return rol_requerido(['empleador', 'trabajador_empleador', 'empresa'])(view_func)


def solo_empresas(view_func):
    """Decorador específico para vistas que solo pueden ver empresas"""
    return rol_requerido(['empresa'])(view_func)