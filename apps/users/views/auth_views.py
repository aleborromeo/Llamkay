# apps/users/views/auth_views.py - CORREGIDO
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse
from django.db import transaction

from apps.users.models import Usuario, Profile, Departamento, Provincia, Distrito
from apps.users.forms import (
    RegisterFormStep1, RegisterFormStep2, RegisterFormStep3,
    RegisterFormStep4, RegisterEmpresaForm
)


@csrf_protect
def login(request):
    """Vista de inicio de sesión"""
    if request.user.is_authenticated:
        return redirect('llamkay:dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Por favor ingresa email y contraseña.")
            return render(request, 'users/auth/login.html')

        try:
            user_obj = User.objects.filter(email=email, is_active=True).first()
            if not user_obj:
                messages.error(request, "Correo o contraseña incorrecta.")
                return render(request, 'users/auth/login.html')

            user = authenticate(request, username=user_obj.username, password=password)
            if user:
                django_login(request, user)
                messages.success(request, f'¡Bienvenido {user.first_name or user.username}!')
                return redirect('llamkay:dashboard')
            else:
                messages.error(request, "Correo o contraseña incorrecta.")
                
        except Exception as e:
            messages.error(request, f"Ocurrió un error: {str(e)}")

    return render(request, 'users/auth/login.html')


def logout_view(request):
    """Vista de cierre de sesión"""
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('llamkay:index')


@csrf_protect
def seleccionar_tipo(request):
    """Vista para seleccionar tipo de usuario antes del registro"""
    if request.method == 'POST':
        tipo = request.POST.get('tipo_usuario')
        if tipo in ['trabajador', 'empleador', 'ambos', 'empresa']:
            request.session['tipo_usuario'] = tipo
            return redirect('users:register')
        else:
            messages.error(request, 'Selecciona una opción válida.')
    
    return render(request, 'users/register/seleccionar_tipo.html')


@csrf_protect
@transaction.atomic
def register(request):
    """Vista Step 1: Registro inicial (email, password, datos básicos)"""
    if 'tipo_usuario' not in request.session:
        return redirect('users:seleccionar_tipo')

    tipo = request.session.get('tipo_usuario', 'trabajador')

    if request.method == 'POST':
        form = RegisterEmpresaForm(request.POST) if tipo == 'empresa' else RegisterFormStep1(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            # Validar contraseñas
            if cd['password1'] != cd['password2']:
                form.add_error('password2', 'Las contraseñas no coinciden.')
                return render(request, 'users/register/step_1.html', {
                    'form': form, 
                    'tipo_usuario': tipo
                })

            # Validar email único
            if User.objects.filter(email=cd['email']).exists():
                form.add_error('email', 'Este correo ya está en uso.')
                return render(request, 'users/register/step_1.html', {
                    'form': form, 
                    'tipo_usuario': tipo
                })

            try:
                # Crear usuario de Django
                username = f"{'empresa' if tipo == 'empresa' else 'user'}_{User.objects.count() + 1}"
                
                user = User.objects.create_user(
                    username=username,
                    email=cd['email'],
                    first_name=cd.get('razon_social', cd.get('nombre', ''))[:30],
                    last_name='' if tipo == 'empresa' else cd.get('apellido', '')[:30],
                    password=cd['password1']
                )

                # Guardar en sesión
                request.session['user_id'] = user.id
                request.session['email'] = cd['email']
                request.session['telefono'] = cd['telefono']
                
                if tipo == 'empresa':
                    request.session['ruc'] = cd['ruc']
                    request.session['razon_social'] = cd['razon_social']
                else:
                    request.session['dni'] = cd['dni']
                    request.session['nombre'] = cd['nombre']
                    request.session['apellido'] = cd['apellido']
                
                messages.success(request, '¡Paso 1 completado! Continúa con tu ubicación.')
                return redirect('users:register_two')

            except Exception as e:
                form.add_error(None, f'Error al crear usuario: {str(e)}')
        else:
            # Mostrar errores del formulario
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegisterEmpresaForm() if tipo == 'empresa' else RegisterFormStep1()

    return render(request, 'users/register/step_1.html', {
        'form': form, 
        'tipo_usuario': tipo
    })


@csrf_protect
def register_two(request):
    """Vista Step 2: Ubicación"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Tu sesión ha expirado. Por favor inicia de nuevo.')
        return redirect('users:register')

    tipo = request.session.get('tipo_usuario')

    if request.method == 'POST':
        form = RegisterFormStep2(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            
            # Guardar en sesión
            request.session['direccion'] = cd['direccion']
            request.session['departamento_id'] = cd['departamento'].id_departamento
            request.session['provincia_id'] = cd['provincia'].id_provincia
            request.session['distrito_id'] = cd['distrito'].id_distrito

            # Si es empleador o empresa, saltar al paso 4
            if tipo in ['empleador', 'empresa']:
                messages.success(request, '¡Casi listo! Solo falta verificar tu identidad.')
                return redirect('users:register_four')
            else:
                messages.success(request, '¡Excelente! Ahora cuéntanos sobre tus habilidades.')
                return redirect('users:register_three')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegisterFormStep2()

    return render(request, 'users/register/step_2.html', {
        'form': form,
        'tipo_usuario': tipo
    })


@csrf_protect
def register_three(request):
    """Vista Step 3: Habilidades y experiencia (solo trabajadores)"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Tu sesión ha expirado.')
        return redirect('users:register')

    tipo = request.session.get('tipo_usuario')

    # Solo para trabajadores
    if tipo not in ['trabajador', 'ambos']:
        return redirect('users:register_four')

    if request.method == 'POST':
        form = RegisterFormStep3(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data

            # Guardar en sesión
            request.session['habilidades'] = cd.get('habilidades', '')
            request.session['disponibilidad'] = cd.get('disponibilidad', '')
            request.session['experiencia'] = cd.get('experiencia', '')
            request.session['estudios'] = cd.get('estudios')
            request.session['carrera'] = cd.get('carrera', '')
            request.session['tarifa'] = str(cd.get('tarifa', 0))

            # Manejar certificaciones (guardar temporalmente)
            # En producción, considera usar almacenamiento temporal o procesarlas en el paso final

            messages.success(request, '¡Perfecto! Un último paso para verificar tu identidad.')
            return redirect('users:register_four')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegisterFormStep3()

    return render(request, 'users/register/step_3.html', {
        'form': form,
        'tipo_usuario': tipo
    })


@csrf_protect
@transaction.atomic
def register_four(request):
    """Vista Step 4: Antecedentes penales y finalización"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Tu sesión ha expirado.')
        return redirect('users:register')

    tipo = request.session.get('tipo_usuario', 'trabajador')

    if request.method == 'POST':
        form = RegisterFormStep4(request.POST, request.FILES)
        
        # Validar que subió archivo
        if 'antecedentes' not in request.FILES:
            messages.error(request, "Debes subir tu constancia de antecedentes penales.")
            return render(request, 'users/register/step_4.html', {'form': form})

        if form.is_valid():
            try:
                # Obtener usuario de Django
                user = User.objects.get(id=user_id)
                
                # Crear Usuario de Llamkay
                usuario, created = Usuario.objects.get_or_create(
                    user=user,
                    defaults={
                        'email': request.session.get('email'),
                        'nombres': request.session.get('nombre', request.session.get('razon_social', '')),
                        'apellidos': request.session.get('apellido', ''),
                        'dni': request.session.get('dni', ''),
                        'telefono': request.session.get('telefono', ''),
                        'tipo_usuario': tipo,
                        'habilitado': True,
                        'verificado': False,  # Pendiente de verificación
                    }
                )

                # Crear Profile
                profile, _ = Profile.objects.get_or_create(
                    id_usuario=usuario,
                    defaults={
                        'bio': request.session.get('habilidades', ''),
                        'tarifa_hora': request.session.get('tarifa', 0),
                    }
                )

                # Asignar ubicación al perfil
                try:
                    if dep_id := request.session.get('departamento_id'):
                        profile.id_departamento = Departamento.objects.get(id_departamento=dep_id)
                    if prov_id := request.session.get('provincia_id'):
                        profile.id_provincia = Provincia.objects.get(id_provincia=prov_id)
                    if dist_id := request.session.get('distrito_id'):
                        profile.id_distrito = Distrito.objects.get(id_distrito=dist_id)
                    profile.save()
                except Exception as e:
                    print(f"Error al asignar ubicación: {str(e)}")

                # Limpiar sesión
                keys_to_delete = [
                    'user_id', 'tipo_usuario', 'dni', 'ruc', 'nombre', 'apellido',
                    'razon_social', 'telefono', 'email', 'direccion',
                    'departamento_id', 'provincia_id', 'distrito_id',
                    'habilidades', 'experiencia', 'disponibilidad', 'estudios',
                    'carrera', 'tarifa'
                ]
                for key in keys_to_delete:
                    request.session.pop(key, None)

                messages.success(
                    request,
                    '¡Registro completado! Tu cuenta está pendiente de verificación. Te notificaremos en 24-48 horas.'
                )
                return redirect('users:login')

            except Exception as e:
                messages.error(request, f'Error al completar registro: {str(e)}')
                print(f"Error en register_four: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegisterFormStep4()

    return render(request, 'users/register/step_4.html', {
        'form': form,
        'tipo_usuario': tipo
    })


def validar_correo(request):
    """API para validar si un correo ya existe"""
    email = request.GET.get('email', '').strip()
    if not email:
        return JsonResponse({'exists': False})
    
    existe = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': existe})