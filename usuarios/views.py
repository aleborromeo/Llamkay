
# ========== IMPORTACIONES ==========
import os, json, logging, traceback

from datetime import datetime, timedelta
from xhtml2pdf import pisa
from io import BytesIO

from django.contrib import messages

from django.http import HttpResponse
from django.contrib.auth import authenticate, login as django_login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.db.models import Avg, Sum, Q
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.template.loader import get_template

from .forms import (
    RegisterFormStep1, RegisterFormStep2, RegisterFormStep3,
    RegisterFormStep4, RegisterEmpresaForm, CalificacionForm
)

from usuarios.models import (
    Usuario, Departamento, Provincia, Distrito, Profile,
    ActividadReciente, Postulacion, Ofertatrabajo, Calificacion,
    UsuarioHabilidad, Certificacion
)

from .utils import (
    extract_text_from_file
)

# ========== CONFIGURACIÓN ==========
logger = logging.getLogger(__name__)
User = get_user_model()

# ========== VISTAS DE USUARIO ==========

# --- AUTENTICACIÓN ---

@csrf_protect
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return render(request, 'usuarios/login.html', {'error_message': "Por favor ingresa email y contraseña."})

        try:
            user_obj = User.objects.filter(email=email, is_active=True).first()
            if not user_obj:
                return render(request, 'usuarios/login.html', {'error_message': "Correo o contraseña incorrecta."})

            user = authenticate(request, username=user_obj.username, password=password)
            if user:
                try:
                    usuario = Usuario.objects.get(user=user)
                    if hasattr(usuario, 'antecedentepenal') and not usuario.antecedentepenal.aprobado:
                        return render(request, 'usuarios/bloqueado_penal.html', {
                            'error_message': 'Tu cuenta está bloqueada por antecedentes penales. Contacta al soporte.'
                        })
                except Usuario.DoesNotExist:
                    pass
                django_login(request, user)
                messages.success(request, f'Bienvenido {user.first_name or user.username}!')
                return redirect('usuarios:dashboard')
            else:
                return render(request, 'usuarios/login.html', {'error_message': "Correo o contraseña incorrecta."})

        except Exception as e:
            return render(request, 'usuarios/login.html', {'error_message': f"Ocurrió un error. {str(e)}"})

    if request.user.is_authenticated:
        return redirect('usuarios:dashboard')

    return render(request, 'usuarios/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('/')

def validar_correo(request):
    email = request.GET.get('email')
    existe = User.objects.filter(email=email).exists()
    return JsonResponse({'exists': existe})

# --- REGISTRO MULTIPASO ---

@csrf_protect
def seleccionar_tipo(request):
    if request.method == 'POST':
        tipo = request.POST.get('tipo_usuario')
        if tipo in ['trabajador', 'empleador', 'trabajador_empleador', 'empresa']:
            request.session['tipo_usuario'] = tipo
            return redirect('usuarios:register')
        else:
            return render(request, 'usuarios/seleccionar_tipo.html', {'error': 'Selecciona una opción válida.'})
    return render(request, 'usuarios/seleccionar_tipo.html')

def register(request, tipo_usuario=None):
    if tipo_usuario:
        request.session['tipo_usuario'] = tipo_usuario

    if 'tipo_usuario' not in request.session:
        return redirect('usuarios:seleccionar_tipo')

    tipo = request.session.get('tipo_usuario', 'trabajador')

    if request.method == 'POST':
        form = RegisterEmpresaForm(request.POST) if tipo == 'empresa' else RegisterFormStep1(request.POST)

        if form.is_valid():
            cd = form.cleaned_data

            if cd['password1'] != cd['password2']:
                form.add_error('password2', 'Las contraseñas no coinciden.')
                return render(request, 'usuarios/register.html', {'form': form, 'tipo_usuario': tipo})

            if User.objects.filter(email=cd['email']).exists():
                form.add_error(None, 'Este correo ya está en uso. Intenta con otro.')
                return render(request, 'usuarios/register.html', {'form': form, 'tipo_usuario': tipo})

            try:
                user = User.objects.create_user(
                    username=f"{'empresa' if tipo == 'empresa' else 'user'}{User.objects.count() + 1}",
                    email=cd['email'],
                    first_name=cd.get('razon_social', cd.get('nombre'))[:30],
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

                return redirect('usuarios:register_two')

            except IntegrityError:
                form.add_error(None, 'Hubo un error al crear el usuario. Inténtalo nuevamente.')
    else:
        form = RegisterEmpresaForm() if tipo == 'empresa' else RegisterFormStep1()

    return render(request, 'usuarios/register.html', {'form': form, 'tipo_usuario': tipo})

def register_two(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('usuarios:register')

    tipo = request.session.get('tipo_usuario')

    if not tipo:
        # Si el tipo no está en sesión, intentamos recuperarlo del usuario creado
        try:
            usuario = Usuario.objects.get(user_id=user_id)
            tipo = usuario.tipo_usuario
            request.session['tipo_usuario'] = tipo
        except Usuario.DoesNotExist:
            # Si no existe usuario todavía, muestra error o corta el bucle
            return render(request, 'usuarios/error.html', {
                'mensaje': 'No se pudo determinar el tipo de usuario. Por favor vuelve a iniciar el registro.'
            })

    if request.method == 'POST':
        form = RegisterFormStep2(request.POST)
        if form.is_valid():
            request.session['direccion'] = form.cleaned_data['direccion']
            request.session['departamento_id'] = form.cleaned_data['departamento'].id_departamento
            request.session['provincia_id'] = form.cleaned_data['provincia'].id_provincia
            request.session['distrito_id'] = form.cleaned_data['distrito'].id_distrito

            return redirect('usuarios:register_four' if tipo in ['empleador', 'empresa'] else 'usuarios:register_three')
    else:
        form = RegisterFormStep2()

    return render(request, 'usuarios/register_two.html', {'form': form})


def register_three(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('usuarios:register')

    tipo = request.session.get('tipo_usuario')
    if not tipo:
        try:
            usuario = Usuario.objects.get(user_id=user_id)
            tipo = usuario.tipo_usuario
            request.session['tipo_usuario'] = tipo
        except Usuario.DoesNotExist:
            return render(request, 'usuarios/error.html', {
                'mensaje': 'No se pudo determinar el tipo de usuario. Por favor vuelve a iniciar el registro.'
            })

    if request.method == 'POST':
        form = RegisterFormStep3(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data

            request.session['habilidades'] = cd.get('habilidades', '')
            request.session['disponibilidad'] = cd.get('disponibilidad', '')
            request.session['experiencia'] = cd.get('experiencia', '')
            request.session['tarifa'] = str(cd.get('tarifa', '')) if cd.get('tarifa') else ''
            request.session['estudios'] = cd.get('estudios')
            request.session['carrera'] = cd.get('carrera', '')

            archivos = request.FILES.getlist('certificaciones')
            request.session['certificaciones_nombres'] = [archivo.name for archivo in archivos]

            return redirect('usuarios:register_four')
    else:
        form = RegisterFormStep3()

    return render(request, 'usuarios/register_three.html', {'form': form})


def register_four(request):
    print(">>> ENTRANDO A register_four")
    print(">>> SESSION KEYS:", list(request.session.keys()))
    
    user_id = request.session.get('user_id')
    if not user_id:
        return render(request, 'usuarios/error.html', {
            'mensaje': 'Tu sesión ha expirado. Vuelve a iniciar el registro.'
        })

    if request.method == 'POST':
        print(">>> POST recibido en register_four")
        print(">>> request.FILES:", request.FILES)

        form = RegisterFormStep4(request.POST, request.FILES)
        
        if 'antecedentes' not in request.FILES:
            return render(request, 'usuarios/register_four.html', {
                'form': form,
                'error': "Debes subir al menos un archivo de antecedentes penales."
            })

        if form.is_valid():
            print(">>> Formulario válido")
            file = request.FILES['antecedentes']
            text = extract_text_from_file(file).upper()

            if any(p in text for p in ["SI REGISTRA", "SÍ REGISTRA", "TIENE ANTECEDENTES"]):
                return render(request, 'usuarios/register_four.html', {
                    'form': form,
                    'error': "Lo sentimos, el documento indica que tienes antecedentes penales. No puedes continuar."
                })

            user = User.objects.get(id=user_id)
            tipo = request.session.get('tipo_usuario', 'trabajador')

            nombres = request.session.get('razon_social', user.first_name or 'Empresa') if tipo == 'empresa' else user.first_name or 'Nombre'
            apellidos = '' if tipo == 'empresa' else user.last_name or 'Apellido'
            dni = request.session.get('ruc', '00000000000') if tipo == 'empresa' else request.session.get('dni', '00000000')

            usuario, creado = Usuario.objects.get_or_create(
                user=user,
                defaults={
                    'nombres': nombres,
                    'apellidos': apellidos,
                    'username': f'user{user.id}',
                    'email': user.email,
                    'telefono': request.session.get('telefono', ''),
                    'clave': '',
                    'dni': dni,
                    'direccion': request.session.get('direccion', ''),
                    'fecha_nacimiento': None,
                    'tipo_usuario': tipo,
                    'habilitado': True,
                }
            )

            if not creado and usuario.tipo_usuario != tipo:
                usuario.tipo_usuario = tipo
                usuario.save()

            profile, _ = Profile.objects.get_or_create(user=user, id_usuario=usuario)
            profile.direccion = request.session.get('direccion', '')

            if dep_id := request.session.get('departamento_id'):
                profile.id_departamento = Departamento.objects.get(id_departamento=dep_id)
            if prov_id := request.session.get('provincia_id'):
                profile.id_provincia = Provincia.objects.get(id_provincia=prov_id)
            if dist_id := request.session.get('distrito_id'):
                profile.id_distrito = Distrito.objects.get(id_distrito=dist_id)

            if tipo == 'trabajador':
                profile.habilidades = request.session.get('habilidades', '')
                profile.redes_sociales = {
                    'disponibilidad': request.session.get('disponibilidad', ''),
                    'experiencia': request.session.get('experiencia', ''),
                    'precio_hora': request.session.get('tarifa', ''),
                    'estudios': request.session.get('estudios'),
                    'carrera': request.session.get('carrera', '')
                }

            if not profile.fecha_registro:
                profile.fecha_registro = now()
                
            print(">>> Guardando profile.redes_sociales con:", profile.redes_sociales)
            profile.save()

            messages.success(request, 'Registro completado con éxito. Ahora puedes iniciar sesión.')
            return redirect('usuarios:login')

        else:
            print(">>> Formulario inválido")
            print(form.errors)
    else:
        form = RegisterFormStep4()
        print(">>> GET recibido - nuevo formulario")

    return render(request, 'usuarios/register_four.html', {'form': form})


# --- PERFIL Y DASHBOARD ---

@login_required
def perfil(request):
    try:
        usuario_db = Usuario.objects.get(user=request.user)
        profile, _ = Profile.objects.get_or_create(user=request.user, id_usuario=usuario_db)

        postulaciones = Postulacion.objects.filter(id_usuario=usuario_db)
        trabajos = Ofertatrabajo.objects.filter(id_oferta__in=postulaciones.values_list('id_oferta', flat=True))

        trabajos_completados = trabajos.filter(estado=True)
        trabajos_activos = trabajos.filter(estado=False)
        calificacion_promedio = Calificacion.objects.filter(id_usuario=usuario_db).aggregate(promedio=Avg('puntuacion'))['promedio'] or 0
        inicio_mes = datetime.now().replace(day=1)
        ingresos_mes = trabajos_completados.filter(fecha_fin__gte=inicio_mes).aggregate(total=Sum('sueldo'))['total'] or 0

        total_completados = trabajos_completados.count()
        satisfechos = Calificacion.objects.filter(id_usuario=usuario_db, puntuacion__gte=4).count()
        porcentaje_satisfechos = (satisfechos / total_completados * 100) if total_completados else 0

        actividades = ActividadReciente.objects.filter(usuario=usuario_db).order_by('-fecha')[:5]
        redes = profile.redes_sociales or {}
        habilidades_usuario = UsuarioHabilidad.objects.filter(id_usuario=usuario_db).select_related('id_habilidad')
        nombres_habilidades = [uh.id_habilidad.nombre for uh in habilidades_usuario]
        certificaciones = Certificacion.objects.filter(usuario=usuario_db)
        calificaciones = Calificacion.objects.filter(id_usuario=usuario_db).select_related('autor')

        context = {
            'usuario': usuario_db,
            'tipo_usuario': usuario_db.tipo_usuario,
            'profile': profile,
            'bio': profile.bio or '',
            'foto_url': profile.foto_url.url if profile.foto_url else '',
            'disponibilidad': redes.get('disponibilidad', ''),
            'precio_hora': redes.get('precio_hora', ''),
            'departamento': profile.id_departamento.nombre if profile.id_departamento else '',
            'provincia': profile.id_provincia.nombre if profile.id_provincia else '',
            'distrito': profile.id_distrito.nombre if profile.id_distrito else '',
            'categorias': profile.categorias,
            'habilidades': nombres_habilidades,
            'certificaciones': certificaciones,
            'calificaciones': calificaciones,
            'estadisticas': {
                'trabajos_realizados': trabajos.count(),
                'trabajos_activos': trabajos_activos.count(),
                'trabajos_completados': total_completados,
                'calificacion': round(calificacion_promedio, 1),
                'porcentaje_satisfechos': round(porcentaje_satisfechos),
                'ingresos_mes': ingresos_mes,
            },
            'trabajos': trabajos.order_by('-fecha_fin'),
            'actividades': actividades,
        }

        return render(request, 'usuarios/perfil.html', context)

    except Usuario.DoesNotExist:
        messages.error(request, "No se encontró tu perfil extendido.")
        return redirect('usuarios:login')

    except Exception as e:
        print(f"Error inesperado en vista perfil: {str(e)}")
        messages.error(request, "Error al cargar el perfil.")
        return redirect('usuarios:dashboard')

@login_required
def dashboard(request):
    try:
        usuario_db = Usuario.objects.get(user=request.user)
        profile, _ = Profile.objects.get_or_create(user=request.user, id_usuario=usuario_db)
        context = {'usuario': usuario_db, 'profile': profile}
        return render(request, 'usuarios/dashboard.html', context)
    except Usuario.DoesNotExist:
        messages.error(request, "No se encontró tu perfil.")
        return redirect('trabajo_llamkay:home')
    
    
# --- EXPORTAR PORTAFOLIO ---

@login_required
def exportar_portafolio_pdf(request):
    try:
        usuario_db = Usuario.objects.get(user=request.user)
        profile = Profile.objects.get(user=request.user)
        
        postulaciones = Postulacion.objects.filter(id_usuario=usuario_db).values_list('id_oferta', flat=True)
        trabajos = Ofertatrabajo.objects.filter(id_oferta__in=postulaciones)
        certificaciones = Certificacion.objects.filter(usuario=usuario_db)

        # Renderizar HTML
        template = get_template('usuarios/portafolio_pdf.html')
        context = {
            'usuario': usuario_db,
            'profile': profile,
            'trabajos': trabajos,
            'certificaciones': certificaciones,
        }
        html = template.render(context)

        # Crear PDF en memoria
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="portafolio.pdf"'
        
        pisa_status = pisa.CreatePDF(BytesIO(html.encode("utf-8")), dest=response)
        if pisa_status.err:
            return HttpResponse('⚠️ Error al generar el PDF', status=500)
        
        return response

    except Exception as e:
        print("Error al exportar portafolio:", e)
        return HttpResponse("Error interno al generar el PDF", status=500)


# --- ACTUALIZAR PERFIL ---

@login_required
@require_POST
@transaction.atomic
def actualizar_perfil(request):
    try:
        usuario_db = Usuario.objects.get(user=request.user)
        profile, _ = Profile.objects.get_or_create(user=request.user, id_usuario=usuario_db)

        telefono = request.POST.get('telefono', '').strip()
        if telefono:
            usuario_db.telefono = telefono
        usuario_db.save()

        descripcion = request.POST.get('descripcion', '').strip()
        if descripcion:
            profile.bio = descripcion

        if 'foto' in request.FILES:
            profile.foto_url = request.FILES['foto']

        for campo, modelo, attr in [
            ('id_departamento', Departamento, 'id_departamento'),
            ('id_provincia', Provincia, 'id_provincia'),
            ('id_distrito', Distrito, 'id_distrito')
        ]:
            valor = request.POST.get(campo)
            if valor:
                setattr(profile, attr, modelo.objects.filter(**{attr: valor}).first())

        redes = profile.redes_sociales or {}
        for campo in ['disponibilidad', 'precio_hora']:
            valor = request.POST.get(campo, '').strip()
            if valor:
                redes[campo] = valor

        profile.redes_sociales = redes
        profile.save()

        return JsonResponse({'status': 'ok', 'message': 'Perfil actualizado correctamente.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    

# --- CALIFICAR USUARIO ---

@login_required
def calificar_usuario(request, usuario_id):
    objetivo = get_object_or_404(Usuario, pk=usuario_id)
    if objetivo == request.user.usuario:        # evita auto‑calificarse
        messages.error(request, "No puedes calificarte a ti mismo.")
        return redirect('usuarios:perfil_publico', usuario_id)

    instancia, _ = Calificacion.objects.get_or_create(
        id_usuario=objetivo,
        autor=request.user.usuario
    )

    if request.method == 'POST':
        form = CalificacionForm(request.POST, instance=instancia)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Gracias por tu calificación!")
            return redirect('usuarios:perfil_publico', usuario_id)
    else:
        form = CalificacionForm(instance=instancia)

    return render(request, 'usuarios/calificar.html', {
        'objetivo': objetivo,
        'form': form
    })


@login_required
def buscar_usuarios(request):
    q = request.GET.get('q', '').strip()
    resultados = []
    if q:
        resultados = Usuario.objects.filter(
            Q(nombres__icontains=q) | Q(apellidos__icontains=q) |
            Q(profile__habilidades__icontains=q)
        ).distinct()
    return render(request, 'usuarios/buscar.html', {
        'query': q,
        'resultados': resultados,
    })

# --- PÁGINAS ESTÁTICAS ---

@login_required
def configuracion(request):
    context = {'user': request.user, 'title': 'Configuración y Privacidad'}
    return render(request, 'usuarios/configuracion.html', context)

@login_required
def ayuda(request):
    context = {'user': request.user, 'title': 'Ayuda y Soporte Técnico'}
    return render(request, 'usuarios/ayuda.html', context)

@login_required
def accesibilidad(request):
    context = {'user': request.user, 'title': 'Pantalla y Accesibilidad'}
    return render(request, 'usuarios/accesibilidad.html', context)

@login_required
def comentarios(request):
    context = {'user': request.user, 'title': 'Enviar Comentarios'}
    return render(request, 'usuarios/comentarios.html', context)


