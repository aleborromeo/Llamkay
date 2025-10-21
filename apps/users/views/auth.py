from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse

from apps.users.models import Usuario, Profile
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
                messages.success(request, f'Bienvenido {user.first_name or user.username}!')
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
def register(request):
    """Vista Step 1: Registro inicial (email, password, datos básicos)"""
    if 'tipo_usuario' not in request.session:
        return redirect('users:seleccionar_tipo')

    tipo = request.session.get('tipo_usuario', 'trabajador')

    if request.method == 'POST':
        form = RegisterEmpresaForm(request.POST) if tipo == 'empresa' else RegisterFormStep1(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            if cd['password1'] != cd['password2']:
                form.add_error('password2', 'Las contraseñas no coinciden.')
                return render(request, 'users/register/step_1.html', {
                    'form': form, 
                    'tipo_usuario': tipo
                })

            if User.objects.filter(email=cd['email']).exists():
                form.add_error(None, 'Este correo ya está en uso.')
                return render(request, 'users/register/step_1.html', {
                    'form': form, 
                    'tipo_usuario': tipo
                })

            try:
                user = User.objects.create_user(
                    username=f"{'empresa' if tipo == 'empresa' else 'user'}{User.objects.count() + 1}",
                    email=cd['email'],
                    first_name=cd.get('razon_social', cd.get('nombre', ''))[:30],
                    last_name='' if tipo == 'empresa' else cd.get('apellido', ''),
                    password=cd['password1']
                )

                request.session['user_id'] = user.id
                request.session['telefono'] = cd['telefono']
                
                if tipo == 'empresa':
                    request.session['ruc'] = cd['ruc']
                    request.session['razon_social'] = cd['razon_social']
                else:
                    request.session['dni'] = cd['dni']
                    request.session['nombre'] = cd['nombre']
                    request.session['apellido'] = cd['apellido']
                
                return redirect('users:register_two')

            except Exception as e:
                form.add_error(None, f'Error: {str(e)}')
    else:
        form = RegisterEmpresaForm() if tipo == 'empresa' else RegisterFormStep1()

    return render(request, 'users/register/step_1.html', {
        'form': form, 
        'tipo_usuario': tipo
    })


def register_two(request):
    """Vista Step 2: Ubicación"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Tu sesión ha expirado.')
        return redirect('users:register')

    tipo = request.session.get('tipo_usuario')

    if request.method == 'POST':
        form = RegisterFormStep2(request.POST)
        if form.is_valid():
            request.session['direccion'] = form.cleaned_data['direccion']
            request.session['departamento_id'] = form.cleaned_data['departamento'].id_departamento
            request.session['provincia_id'] = form.cleaned_data['provincia'].id_provincia
            request.session['distrito_id'] = form.cleaned_data['distrito'].id_distrito

            if tipo in ['empleador', 'empresa']:
                return redirect('users:register_four')
            else:
                return redirect('users:register_three')
    else:
        form = RegisterFormStep2()

    return render(request, 'users/register/step_2.html', {
        'form': form,
        'tipo_usuario': tipo
    })


def register_three(request):
    """Vista Step 3: Habilidades y experiencia (solo trabajadores)"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Tu sesión ha expirado.')
        return redirect('users:register')

    tipo = request.session.get('tipo_usuario')

    if request.method == 'POST':
        form = RegisterFormStep3(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data

            request.session['habilidades'] = cd.get('habilidades', '')
            request.session['disponibilidad'] = cd.get('disponibilidad', '')
            request.session['experiencia'] = cd.get('experiencia', '')
            request.session['estudios'] = cd.get('estudios')
            request.session['carrera'] = cd.get('carrera', '')

            return redirect('users:register_four')
    else:
        form = RegisterFormStep3()

    return render(request, 'users/register/step_3.html', {
        'form': form,
        'tipo_usuario': tipo
    })


def register_four(request):
    """Vista Step 4: Antecedentes penales y finalización"""
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Tu sesión ha expirado.')
        return redirect('users:register')

    if request.method == 'POST':
        form = RegisterFormStep4(request.POST, request.FILES)
        
        if 'antecedentes' not in request.FILES:
            messages.error(request, "Debes subir antecedentes penales.")
            return render(request, 'users/register/step_4.html', {'form': form})

        if form.is_valid():
            # Aquí procesarías el archivo de antecedentes
            # (Validación con OCR/IA si es necesario)
            
            user = User.objects.get(id=user_id)
            tipo = request.session.get('tipo_usuario', 'trabajador')

            # Crear Usuario y Profile
            from apps.users.models import Usuario, Profile, Departamento, Provincia, Distrito
            
            usuario, _ = Usuario.objects.get_or_create(
                user=user,
                defaults={
                    'nombres': request.session.get('nombre', user.first_name),
                    'apellidos': request.session.get('apellido', user.last_name),
                    'username': user.username,
                    'email': user.email,
                    'telefono': request.session.get('telefono', ''),
                    'dni': request.session.get('dni', ''),
                    'tipo_usuario': tipo,
                    'habilitado': True,
                }
            )

            profile, _ = Profile.objects.get_or_create(
                user=user,
                id_usuario=usuario
            )

            # Guardar ubicación
            if dep_id := request.session.get('departamento_id'):
                profile.id_departamento = Departamento.objects.get(id_departamento=dep_id)
            if prov_id := request.session.get('provincia_id'):
                profile.id_provincia = Provincia.objects.get(id_provincia=prov_id)
            if dist_id := request.session.get('distrito_id'):
                profile.id_distrito = Distrito.objects.get(id_distrito=dist_id)

            profile.save()

            messages.success(request, 'Registro completado. ¡Bienvenido!')
            return redirect('users:login')
    else:
        form = RegisterFormStep4()

    return render(request, 'users/register/step_4.html', {'form': form})


def validar_correo(request):
    """API para validar si un correo ya existe"""
    email = request.GET.get('email')
    existe = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': existe})