"""
Vistas para el módulo de gestión de trabajos - CORREGIDO
"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string
from datetime import time

from .models import OfertaUsuario, OfertaEmpresa, GuardarTrabajo
from .forms import OfertaUsuarioForm, OfertaEmpresaForm
from apps.users.models import Departamento, Provincia, Distrito, Comunidad, Usuario


# ==================== REGISTRO DE OFERTAS ====================

@login_required
def registro_individual(request):
    """
    Vista para registrar ofertas de trabajo como usuario individual.
    Solo accesible para usuarios con tipo 'ofrecer-trabajo' o 'ambos'.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.tipo_usuario not in ['ofrecer-trabajo', 'ambos']:
        raise PermissionDenied("No tienes permiso para registrar una oferta como usuario individual.")

    if request.method == 'POST':
        form = OfertaUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.empleador = request.user

            # Procesar hora límite (formato 12h con AM/PM)
            try:
                hora = int(request.POST.get('hora', 0))
                minuto = int(request.POST.get('minuto', 0))
                segundo = int(request.POST.get('segundo', 0))
                ampm = request.POST.get('ampm', 'AM').upper()

                # Convertir a formato 24h
                if ampm == 'PM' and hora != 12:
                    hora += 12
                if ampm == 'AM' and hora == 12:
                    hora = 0

                oferta.horas_limite = time(hora, minuto, segundo)
            except Exception as e:
                form.add_error(None, f"Error al procesar la hora límite: {str(e)}")
                return render(request, 'jobs/registro_individual.html', {
                    'form': form,
                    'horas': ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],
                    'tiempos': ["00", "15", "30", "45"],
                })

            oferta.save()
            messages.success(request, "Oferta registrada exitosamente.")
            return redirect('jobs:all_trabajos')
    else:
        form = OfertaUsuarioForm()
        horas = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
        tiempos = ["00", "15", "30", "45"]

    return render(request, 'jobs/registro_individual.html', {
        'form': form,
        'horas': horas,
        'tiempos': tiempos,
    })


@login_required
def registro_empresa(request):
    """
    Vista para registrar ofertas de trabajo como empresa.
    Solo accesible para usuarios con tipo 'empresa'.
    """
    if not hasattr(request.user, 'profile') or request.user.profile.tipo_usuario != 'empresa':
        raise PermissionDenied("No tienes permiso para registrar una oferta como empresa.")

    if request.method == 'POST':
        form = OfertaEmpresaForm(request.POST, request.FILES)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.empleador = request.user
            oferta.save()
            messages.success(request, "Oferta de empresa registrada exitosamente.")
            return redirect('jobs:all_trabajos')
    else:
        form = OfertaEmpresaForm()

    departamentos = Departamento.objects.all()

    return render(request, 'jobs/registro_empresa.html', {
        'form': form,
        'departamentos': departamentos,
    })


# ==================== LISTADO Y BÚSQUEDA DE TRABAJOS ====================

def all_trabajos(request):
    """
    Vista principal que muestra todos los trabajos activos.
    Combina ofertas de usuarios y empresas.
    """
    # ✅ CORREGIDO: 'empleador__profile' en vez de 'empleador__perfil'
    ofertas_usuario = OfertaUsuario.objects.select_related(
        'empleador',
        'empleador__profile',  # ✅ Corregido
        'empleador__empresa',
        'id_departamento', 
        'id_provincia', 
        'id_distrito', 
        'id_comunidad'
    ).filter(estado='activa')

    ofertas_empresa = OfertaEmpresa.objects.select_related(
        'empleador',
        'empleador__profile',  # ✅ Corregido
        'empleador__empresa', 
        'id_departamento', 
        'id_provincia', 
        'id_distrito', 
        'id_comunidad'
    ).filter(estado='activa')

    trabajos = []

    # Procesar ofertas de usuarios
    for o in ofertas_usuario:
        profile = getattr(o.empleador, 'profile', None)  # ✅ Corregido
        
        if profile and profile.tipo_usuario == 'empresa' and hasattr(o.empleador, 'empresa'):
            publicado_por = o.empleador.empresa.nombre_empresa
        elif profile:
            publicado_por = f"{profile.nombres} {profile.apellidos}"
        else:
            publicado_por = "Usuario"

        trabajos.append({
            'tipo': 'usuario',
            'id': o.id,
            'titulo': o.titulo,
            'descripcion': o.descripcion,
            'herramientas': o.herramientas,
            'pago': o.pago,
            'foto': o.foto,
            'fecha_registro': o.fecha_registro,
            'fecha_limite': o.fecha_limite,
            'horas_limite': o.horas_limite,
            'rango_salarial': None,
            'experiencia_requerida': None,
            'modalidad_trabajo': None,
            'requisitos_calificaciones': None,
            'beneficios_compensaciones': None,
            'numero_postulantes': None,
            'numero_contacto': o.numero_contacto,
            'id_departamento': o.id_departamento,
            'id_provincia': o.id_provincia,
            'id_distrito': o.id_distrito,
            'id_comunidad': o.id_comunidad,
            'publicado_por': publicado_por,
        })

    # Procesar ofertas de empresas
    for o in ofertas_empresa:
        empresa = getattr(o.empleador, 'empresa', None)
        publicado_por = empresa.nombre_empresa if empresa else "Empresa"

        trabajos.append({
            'tipo': 'empresa',
            'id': o.id,
            'titulo': o.titulo_puesto,
            'descripcion': o.descripcion_puesto,
            'herramientas': None,
            'pago': None,
            'foto': o.foto,
            'fecha_registro': o.fecha_registro,
            'fecha_limite': o.fecha_limite,
            'horas_limite': None,
            'rango_salarial': o.rango_salarial,
            'experiencia_requerida': o.experiencia_requerida,
            'modalidad_trabajo': o.modalidad_trabajo,
            'requisitos_calificaciones': o.requisitos_calificaciones,
            'beneficios_compensaciones': o.beneficios_compensaciones,
            'numero_postulantes': o.numero_postulantes,
            'numero_contacto': o.numero_contacto,
            'id_departamento': o.id_departamento,
            'id_provincia': o.id_provincia,
            'id_distrito': o.id_distrito,
            'id_comunidad': o.id_comunidad,
            'publicado_por': publicado_por,
        })

    # Obtener trabajos guardados por el usuario autenticado
    trabajos_guardados = set()
    if request.user.is_authenticated and hasattr(request.user, 'profile'):  # ✅ Corregido
        try:
            usuario = request.user
            guardados = GuardarTrabajo.objects.filter(usuario=usuario)
            for g in guardados:
                trabajos_guardados.add(f"{g.content_type.model}_{g.object_id}")
        except Exception:
            pass

    # Ordenar trabajos por fecha de registro
    trabajos.sort(key=lambda x: x['fecha_registro'], reverse=True)

    departamentos = Departamento.objects.all()

    return render(request, "jobs/all_trabajos.html", {
        'trabajos': trabajos,
        'departamentos': departamentos,
        'trabajos_guardados_ids': trabajos_guardados,
    })


def filtrar_trabajos(request):
    """
    Vista para filtrar trabajos según diferentes criterios:
    - Búsqueda por texto
    - Ubicación (departamento, provincia, distrito, comunidad)
    - Tipo de usuario (empleador/empresa)
    """
    buscar = request.GET.get('buscar', '')
    departamento_id = request.GET.get('departamento_id')
    provincia_id = request.GET.get('provincia_id')
    distrito_id = request.GET.get('distrito_id')
    comunidad_id = request.GET.get('comunidad_id')
    tipo_usuario = request.GET.get('tipo_usuario')

    trabajos = []

    # ----- FILTRAR OFERTAS DE USUARIOS -----
    if tipo_usuario in ('', 'empleador'):
        # ✅ CORREGIDO: 'empleador__profile'
        queryset = OfertaUsuario.objects.select_related(
            'empleador',
            'empleador__profile',  # ✅ Corregido
            'empleador__empresa'
        ).filter(estado='activa')

        if buscar:
            queryset = queryset.filter(
                Q(titulo__icontains=buscar) | Q(descripcion__icontains=buscar)
            )
        if departamento_id:
            queryset = queryset.filter(id_departamento=departamento_id)
        if provincia_id:
            queryset = queryset.filter(id_provincia=provincia_id)
        if distrito_id:
            queryset = queryset.filter(id_distrito=distrito_id)
        if comunidad_id:
            queryset = queryset.filter(id_comunidad=comunidad_id)

        for o in queryset:
            profile = getattr(o.empleador, 'profile', None)  # ✅ Corregido
            empresa = getattr(o.empleador, 'empresa', None)

            if profile and profile.tipo_usuario == 'empresa' and empresa:
                publicado_por = empresa.nombre_empresa
            elif profile:
                publicado_por = f"{profile.nombres} {profile.apellidos}"
            else:
                publicado_por = "Usuario"

            trabajos.append({
                'id': o.id,
                'tipo': 'usuario',
                'titulo': o.titulo,
                'descripcion': o.descripcion,
                'herramientas': o.herramientas,
                'pago': o.pago,
                'foto': o.foto,
                'fecha_registro': o.fecha_registro,
                'fecha_limite': o.fecha_limite,
                'horas_limite': o.horas_limite,
                'rango_salarial': None,
                'experiencia_requerida': None,
                'modalidad_trabajo': None,
                'requisitos_calificaciones': None,
                'beneficios_compensaciones': None,
                'numero_postulantes': None,
                'numero_contacto': o.numero_contacto,
                'id_departamento': o.id_departamento,
                'id_provincia': o.id_provincia,
                'id_distrito': o.id_distrito,
                'id_comunidad': o.id_comunidad,
                'publicado_por': publicado_por,
            })

    # ----- FILTRAR OFERTAS DE EMPRESAS -----
    if tipo_usuario in ('', 'empresa'):
        queryset = OfertaEmpresa.objects.select_related(
            'empleador',
            'empleador__empresa'
        ).filter(estado='activa')

        if buscar:
            queryset = queryset.filter(
                Q(titulo_puesto__icontains=buscar) | Q(descripcion_puesto__icontains=buscar)
            )
        if departamento_id:
            queryset = queryset.filter(id_departamento=departamento_id)
        if provincia_id:
            queryset = queryset.filter(id_provincia=provincia_id)
        if distrito_id:
            queryset = queryset.filter(id_distrito=distrito_id)
        if comunidad_id:
            queryset = queryset.filter(id_comunidad=comunidad_id)

        for o in queryset:
            empresa = getattr(o.empleador, 'empresa', None)
            publicado_por = empresa.nombre_empresa if empresa else "Empresa"

            trabajos.append({
                'id': o.id,
                'tipo': 'empresa',
                'titulo': o.titulo_puesto,
                'descripcion': o.descripcion_puesto,
                'herramientas': None,
                'pago': None,
                'foto': o.foto,
                'fecha_registro': o.fecha_registro,
                'fecha_limite': o.fecha_limite,
                'horas_limite': None,
                'rango_salarial': o.rango_salarial,
                'experiencia_requerida': o.experiencia_requerida,
                'modalidad_trabajo': o.modalidad_trabajo,
                'requisitos_calificaciones': o.requisitos_calificaciones,
                'beneficios_compensaciones': o.beneficios_compensaciones,
                'numero_postulantes': o.numero_postulantes,
                'numero_contacto': o.numero_contacto,
                'id_departamento': o.id_departamento,
                'id_provincia': o.id_provincia,
                'id_distrito': o.id_distrito,
                'id_comunidad': o.id_comunidad,
                'publicado_por': publicado_por,
            })

    # Ordenar por fecha
    trabajos.sort(key=lambda x: x['fecha_registro'], reverse=True)

    departamentos = Departamento.objects.all()

    return render(request, "jobs/all_trabajos.html", {
        'trabajos': trabajos,
        'departamentos': departamentos
    })


# ==================== ADMINISTRACIÓN DE TRABAJOS (EMPLEADOR) ====================

@login_required
def mis_trabajos(request):
    """
    Vista que muestra todos los trabajos publicados por el empleador actual.
    """
    usuario = request.user
    trabajos_usuario = list(OfertaUsuario.objects.filter(empleador=usuario))
    trabajos_empresa = list(OfertaEmpresa.objects.filter(empleador=usuario))
    trabajos = trabajos_usuario + trabajos_empresa
    
    return render(request, 'jobs/trabajos_empleador.html', {'trabajos': trabajos})


@login_required
def mis_trabajos_ajax(request):
    """
    Vista AJAX para cargar dinámicamente los trabajos del empleador.
    """
    usuario = request.user
    trabajos_usuario = list(OfertaUsuario.objects.filter(empleador=usuario))
    trabajos_empresa = list(OfertaEmpresa.objects.filter(empleador=usuario))
    trabajos = trabajos_usuario + trabajos_empresa
    
    return render(request, 'jobs/trabajos_empleador.html', {'trabajos': trabajos})


@login_required
def editar_trabajo(request, oferta_id):
    """
    Vista para editar una oferta de trabajo existente.
    Detecta automáticamente si es OfertaUsuario u OfertaEmpresa.
    """
    usuario = request.user

    # Intentar obtener como OfertaUsuario
    trabajo = OfertaUsuario.objects.filter(id=oferta_id, empleador=usuario).first()
    if trabajo:
        form_class = OfertaUsuarioForm
        template = 'jobs/registro_individual.html'
        context_extra = {
            'horas': ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],
            'tiempos': ["00", "15", "30", "45"],
        }
    else:
        # Intentar obtener como OfertaEmpresa
        trabajo = OfertaEmpresa.objects.filter(id=oferta_id, empleador=usuario).first()
        if not trabajo:
            raise PermissionDenied("No tienes permiso para editar este trabajo.")
        form_class = OfertaEmpresaForm
        template = 'jobs/registro_empresa.html'
        context_extra = {}

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=trabajo)
        if form.is_valid():
            # Si es OfertaUsuario, procesar la hora límite
            if isinstance(trabajo, OfertaUsuario):
                try:
                    hora = int(request.POST.get('hora', 0))
                    minuto = int(request.POST.get('minuto', 0))
                    segundo = int(request.POST.get('segundo', 0))
                    ampm = request.POST.get('ampm', 'AM').upper()

                    if ampm == 'PM' and hora != 12:
                        hora += 12
                    if ampm == 'AM' and hora == 12:
                        hora = 0

                    trabajo.horas_limite = time(hora, minuto, segundo)
                except Exception:
                    form.add_error(None, "Error al procesar la hora límite.")
                    return render(request, template, {
                        'form': form,
                        'modo_edicion': True,
                        **context_extra
                    })
            
            form.save()
            messages.success(request, "Trabajo actualizado exitosamente.")
            return redirect('jobs:mis_trabajos')
    else:
        form = form_class(instance=trabajo)

    return render(request, template, {
        'form': form,
        'modo_edicion': True,
        **context_extra
    })


@login_required
def eliminar_trabajo(request, oferta_id):
    """
    Vista para eliminar una oferta de trabajo.
    Verifica que el usuario sea el propietario.
    """
    usuario = request.user
    
    # Buscar en ambos modelos
    trabajo = OfertaUsuario.objects.filter(id=oferta_id, empleador=usuario).first()
    if not trabajo:
        trabajo = OfertaEmpresa.objects.filter(id=oferta_id, empleador=usuario).first()
    
    if not trabajo:
        messages.error(request, "No tienes permiso para eliminar este trabajo.")
        return redirect('jobs:mis_trabajos')

    if request.method == 'POST':
        trabajo.delete()
        messages.success(request, "Trabajo eliminado correctamente.")
        return redirect('jobs:mis_trabajos')
    
    # Si no es POST, mostrar confirmación
    return render(request, 'jobs/confirmar_eliminar.html', {'trabajo': trabajo})


# ==================== AJAX PARA UBICACIÓN ====================

def cargar_provincias(request):
    """
    Vista AJAX para cargar provincias según departamento seleccionado.
    """
    departamento_id = request.GET.get('departamento_id')
    provincias = Provincia.objects.filter(
        id_departamento=departamento_id
    ).values('id_provincia', 'nombre')
    return JsonResponse(list(provincias), safe=False)


def cargar_distritos(request):
    """
    Vista AJAX para cargar distritos según provincia seleccionada.
    """
    provincia_id = request.GET.get('provincia_id')
    distritos = Distrito.objects.filter(
        id_provincia=provincia_id
    ).values('id_distrito', 'nombre')
    return JsonResponse(list(distritos), safe=False)


def cargar_comunidades(request):
    """
    Vista AJAX para cargar comunidades según distrito seleccionado.
    """
    distrito_id = request.GET.get('distrito_id')
    comunidades = Comunidad.objects.filter(
        id_distrito=distrito_id
    ).values('id_comunidad', 'nombre')
    return JsonResponse(list(comunidades), safe=False)


# ==================== DASHBOARD TRABAJADOR (BUSCAR TRABAJO) ====================

@login_required
def dashboard_trabajador(request):
    """
    Dashboard para usuarios que buscan trabajo.
    Muestra trabajos guardados y recomendaciones.
    """
    if not hasattr(request.user, 'profile'):  # ✅ Corregido
        messages.error(request, "Tu perfil de usuario no está completo.")
        return redirect('users:login')
    
    usuario = request.user
    profile = request.user.profile  # ✅ Corregido
    
    # Verificar que sea un usuario buscador
    if profile.tipo_usuario not in ['buscar-trabajo', 'ambos']:
        messages.error(request, "No tienes permiso para acceder al dashboard de trabajador.")
        return redirect('jobs:all_trabajos')
    
    return render(request, 'jobs/dashboard_trabajador.html', {
        'usuario': usuario,
        'profile': profile
    })


@login_required
def guardar_trabajo(request, tipo_oferta, oferta_id):
    """
    Vista para guardar una oferta de trabajo como favorita.
    Solo usuarios 'buscar-trabajo' o 'ambos' pueden guardar trabajos.
    """
    if not hasattr(request.user, 'profile'):  # ✅ Corregido
        messages.error(request, "Tu perfil de usuario no está completo.")
        return redirect('users:login')

    usuario = request.user
    profile = request.user.profile  # ✅ Corregido

    # Verificar permisos
    if profile.tipo_usuario not in ['buscar-trabajo', 'ambos']:
        messages.error(request, "No tienes permiso para guardar trabajos.")
        return redirect('jobs:all_trabajos')

    # Determinar el modelo según tipo
    if tipo_oferta == 'usuario':
        oferta_model = OfertaUsuario
    elif tipo_oferta == 'empresa':
        oferta_model = OfertaEmpresa
    else:
        messages.error(request, "Tipo de oferta no válido.")
        return redirect('jobs:all_trabajos')

    oferta = get_object_or_404(oferta_model, id=oferta_id)
    content_type = ContentType.objects.get_for_model(oferta)

    # Verificar si ya está guardado
    ya_guardado = GuardarTrabajo.objects.filter(
        usuario=usuario,
        content_type=content_type,
        object_id=oferta.id
    ).exists()

    if ya_guardado:
        messages.info(request, "Ya habías guardado esta oferta.")
    else:
        GuardarTrabajo.objects.create(
            usuario=usuario,
            content_type=content_type,
            object_id=oferta.id
        )
        messages.success(request, "Trabajo guardado exitosamente.")

    # Redirigir según de dónde viene
    next_url = request.GET.get('next', 'jobs:dashboard_trabajador')
    return redirect(next_url)


@login_required
def trabajos_guardados(request):
    """
    Vista que muestra todos los trabajos guardados por el usuario.
    """
    if not hasattr(request.user, 'profile'):  # ✅ Corregido
        messages.error(request, "Tu perfil de usuario no está completo.")
        return redirect('users:login')
    
    usuario = request.user
    trabajos_guardados = GuardarTrabajo.objects.filter(
        usuario=usuario
    ).select_related('content_type').order_by('-fecha_guardado')
    
    return render(request, 'jobs/trabajos_guardados.html', {
        'trabajos': trabajos_guardados
    })


@login_required
def trabajos_guardados_ajax(request):
    """
    Vista AJAX para cargar dinámicamente los trabajos guardados.
    """
    if not hasattr(request.user, 'profile'):  # ✅ Corregido
        return JsonResponse({'error': 'Perfil no encontrado'}, status=400)
    
    usuario = request.user
    trabajos_guardados = GuardarTrabajo.objects.filter(
        usuario=usuario
    ).select_related('content_type').order_by('-fecha_guardado')

    html = render_to_string('jobs/trabajos_guardados.html', {
        'trabajos': trabajos_guardados
    }, request=request)

    return JsonResponse({'html': html})


@login_required
def quitar_guardado(request, id=None):
    """
    Vista para quitar un trabajo de la lista de guardados.
    Puede recibir el ID directamente o los parámetros content_type y object_id.
    """
    if request.method != "POST":
        return redirect('jobs:dashboard_trabajador')

    usuario = request.user

    # Opción 1: Eliminar por ID de GuardarTrabajo
    if id:
        GuardarTrabajo.objects.filter(id=id, usuario=usuario).delete()
        messages.success(request, "Trabajo eliminado de guardados.")
        return redirect('jobs:trabajos_guardados')

    # Opción 2: Eliminar por content_type y object_id
    content_type_id = request.POST.get("content_type_id")
    object_id = request.POST.get("object_id")

    if not content_type_id or not object_id:
        messages.error(request, "Datos incompletos.")
        return redirect('jobs:dashboard_trabajador')

    try:
        content_type = ContentType.objects.get(id=content_type_id)
        model_class = content_type.model_class()
        oferta = model_class.objects.get(id=object_id)
        
        GuardarTrabajo.objects.filter(
            usuario=usuario,
            content_type=content_type,
            object_id=oferta.id
        ).delete()
        
        messages.success(request, "Trabajo eliminado de guardados.")
    except Exception as e:
        messages.error(request, f"Error al eliminar: {str(e)}")

    return redirect('jobs:dashboard_trabajador')