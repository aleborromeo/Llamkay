from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,render, get_object_or_404
from django.core.exceptions import PermissionDenied
from trabajos.models import OfertaUsuario
from trabajos.forms import OfertaUsuarioForm 
from trabajos.models import OfertaEmpresa, GuardarTrabajo
from trabajos.forms import OfertaEmpresaForm 
from datetime import time
from django.http import JsonResponse
from usuarios.models import Departamento, Provincia, Distrito, Comunidad,Usuario
from django.contrib import messages
from itertools import chain
from django.utils.timezone import now
from django.db.models import Q
from django.contrib.contenttypes.models import ContentType
from django.template.loader import render_to_string




@login_required
def registro_individual(request):
    # Corregido: acceder al perfil del usuario
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo_usuario not in ['ofrecer-trabajo', 'ambos']:
        raise PermissionDenied("No tienes permiso para registrar una oferta como usuario individual.")

    if request.method == 'POST':
        form = OfertaUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.empleador = request.user.perfil  # <- corregido: empleador es un Usuario

            try:
                hora = int(request.POST.get('hora', 0))
                minuto = int(request.POST.get('minuto', 0))
                segundo = int(request.POST.get('segundo', 0))
                ampm = request.POST.get('ampm', 'AM').upper()

                if ampm == 'PM' and hora != 12:
                    hora += 12
                if ampm == 'AM' and hora == 12:
                    hora = 0

                oferta.horas_limite = time(hora, minuto, segundo)
            except Exception:
                form.add_error(None, "Error al procesar la hora límite.")
                return render(request, 'trabajos/registro_individual.html', {
                    'form': form,
                    'horas': ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"],
                    'tiempos': ["00", "15", "30", "45"],
                })

            oferta.save()
            return redirect('trabajos:all_trabajos')
    else:
        form = OfertaUsuarioForm()

    horas = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    tiempos = ["00", "15", "30", "45"]

    return render(request, 'trabajos/registro_individual.html', {
        'form': form,
        'horas': horas,
        'tiempos': tiempos,
    })

@login_required
def registro_empresa(request):
    # Corregido: acceder al perfil del usuario
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo_usuario != 'empresa':
        raise PermissionDenied("No tienes permiso para registrar una oferta como empresa.")

    if request.method == 'POST':
        form = OfertaEmpresaForm(request.POST, request.FILES)
        if form.is_valid():
            oferta = form.save(commit=False)
            oferta.empleador = request.user.perfil  # <- corregido
            oferta.save()
            return redirect('trabajos:all_trabajos')
    else:
        form = OfertaEmpresaForm()

    departamentos = Departamento.objects.all()

    return render(request, 'trabajos/registro_empresa.html', {
        'form': form,
        'departamentos': departamentos,
    })


def all_trabajos(request):
    ofertas_usuario = OfertaUsuario.objects.select_related(
        'empleador__profile', 'id_departamento', 'id_provincia', 'id_distrito', 'id_comunidad'
    ).filter(estado='activa')

    ofertas_empresa = OfertaEmpresa.objects.select_related(
        'empleador__profile', 'empleador__empresa', 'id_departamento', 'id_provincia', 'id_distrito', 'id_comunidad'
    ).filter(estado='activa')

    trabajos = []

    for o in ofertas_usuario:
        perfil = getattr(o.empleador, 'perfil', None)
        if perfil and perfil.tipo_usuario == 'empresa' and hasattr(o.empleador, 'empresa'):
            publicado_por = o.empleador.empresa.nombre_empresa
        elif perfil:
            publicado_por = f"{perfil.nombres} {perfil.apellidos}"
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

    # Obtener trabajos guardados por el usuario
    trabajos_guardados = set()  # Usamos set para búsquedas rápidas
    if request.user.is_authenticated:
        try:
            usuario = request.user.perfil  # Accede al modelo Usuario
            guardados = GuardarTrabajo.objects.filter(usuario=usuario)
            for g in guardados:
                trabajos_guardados.add(f"{g.content_type.model}_{g.object_id}")
        except Usuario.DoesNotExist:
            pass
        pass



    departamentos = Departamento.objects.all()

    return render(request, "trabajos/all_trabajos.html", {
        'trabajos': trabajos,
        'departamentos': departamentos,
        'trabajos_guardados_ids': trabajos_guardados,
    })

    


def filtrar_trabajos(request):
    buscar = request.GET.get('buscar', '')
    departamento_id = request.GET.get('departamento_id')
    provincia_id = request.GET.get('provincia_id')
    distrito_id = request.GET.get('distrito_id')
    comunidad_id = request.GET.get('comunidad_id')
    tipo_usuario = request.GET.get('tipo_usuario')

    trabajos = []

    # ----- FILTRAR USUARIOS -----
    if tipo_usuario in ('', 'empleador'):
        queryset = OfertaUsuario.objects.select_related('empleador__user', 'empleador__empresa').filter(estado='activa')

        if buscar:
            queryset = queryset.filter(Q(titulo__icontains=buscar) | Q(descripcion__icontains=buscar))
        if departamento_id:
            queryset = queryset.filter(id_departamento=departamento_id)
        if provincia_id:
            queryset = queryset.filter(id_provincia=provincia_id)
        if distrito_id:
            queryset = queryset.filter(id_distrito=distrito_id)
        if comunidad_id:
            queryset = queryset.filter(id_comunidad=comunidad_id)

        for o in queryset:
            perfil = getattr(o.empleador, 'perfil', None)
            empresa = getattr(o.empleador, 'empresa', None)

            if perfil and perfil.tipo_usuario == 'empresa' and empresa:
                publicado_por = empresa.nombre_empresa
            elif perfil:
                publicado_por = f"{perfil.nombres} {perfil.apellidos}"
            else:
                publicado_por = "Usuario"

            trabajos.append({
                'id': o.id,  # ✅ clave agregada
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

    # ----- FILTRAR EMPRESAS -----
    if tipo_usuario in ('', 'empresa'):
        queryset = OfertaEmpresa.objects.select_related('empleador__empresa').filter(estado='activa')

        if buscar:
            queryset = queryset.filter(Q(titulo_puesto__icontains=buscar) | Q(descripcion_puesto__icontains=buscar))
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
                'id': o.id,  # ✅ clave agregada
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

    departamentos = Departamento.objects.all()

    return render(request, "trabajos/all_trabajos.html", {
        'trabajos': trabajos,
        'departamentos': departamentos
    })
















def admin_empleador(request):
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo_usuario not in ['ofrecer-trabajo', 'ambos']:
        raise PermissionDenied("No tienes permiso para acceder a esta sección.")

    usuario = request.user.perfil  # accedemos al modelo personalizado

    ofertas_usuario = OfertaUsuario.objects.filter(empleador=usuario, estado='activa')
    ofertas_empresa = OfertaEmpresa.objects.filter(empleador=usuario, estado='activa')

    return render(request, 'trabajos/admin_empleador.html', {
        'ofertas_usuario': ofertas_usuario,
        'ofertas_empresa': ofertas_empresa,
    })

def admin_empresa(request):
    if not hasattr(request.user, 'perfil') or request.user.perfil.tipo_usuario != 'empresa':
        raise PermissionDenied("No tienes permiso para acceder a esta sección.")

    usuario = request.user.perfil

    ofertas_empresa = OfertaEmpresa.objects.filter(empleador=usuario, estado='activa')

    return render(request, 'trabajos/admin_empresa.html', {
        'ofertas_empresa': ofertas_empresa,
    })
    
@login_required
def mis_trabajos(request):
    usuario = request.user.perfil
    trabajos_usuario = list(OfertaUsuario.objects.filter(empleador=usuario))
    trabajos_empresa = list(OfertaEmpresa.objects.filter(empleador=usuario))
    trabajos = trabajos_usuario + trabajos_empresa
    return render(request, 'trabajos/trabajos_empleador.html', {'trabajos': trabajos})

@login_required
def mis_trabajos_ajax(request):
    usuario = request.user.perfil
    trabajos_usuario = list(OfertaUsuario.objects.filter(empleador=usuario))
    trabajos_empresa = list(OfertaEmpresa.objects.filter(empleador=usuario))
    trabajos = trabajos_usuario + trabajos_empresa
    return render(request, 'trabajos/trabajos_empleador.html', {'trabajos': trabajos})


@login_required
def editar_trabajo(request, oferta_id):
    usuario = request.user.perfil

    # Intenta obtener trabajo como OfertaUsuario
    trabajo = OfertaUsuario.objects.filter(id=oferta_id, empleador=usuario).first()
    if trabajo:
        form_class = OfertaUsuarioForm
        template = 'trabajos/registro_individual.html'
    else:
        # Intenta obtener como OfertaEmpresa
        trabajo = OfertaEmpresa.objects.filter(id=oferta_id, empleador=usuario).first()
        if not trabajo:
            raise PermissionDenied("No tienes permiso para editar este trabajo.")
        form_class = OfertaEmpresaForm
        template = 'trabajos/registro_empresa.html'

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=trabajo)
        if form.is_valid():
            form.save()
            return redirect('trabajos:all_trabajos')
    else:
        form = form_class(instance=trabajo)

    return render(request, template, {
        'form': form,
        'modo_edicion': True,
        
    })


@login_required
def eliminar_trabajo(request, id):
    trabajo = get_object_or_404(OfertaUsuario, id=id)

    # Asegura que solo el creador pueda eliminar
    if trabajo.empleador != request.user:
        messages.error(request, "No tienes permiso para eliminar este trabajo.")
        return redirect('trabajos:mis_trabajos')

    trabajo.delete()
    messages.success(request, "Trabajo eliminado correctamente.")
    return redirect('trabajos:mis_trabajos')



#----------
def cargar_provincias(request):
    departamento_id = request.GET.get('departamento_id')
    provincias = Provincia.objects.filter(id_departamento=departamento_id).values('id_provincia', 'nombre')
    return JsonResponse(list(provincias), safe=False)

def cargar_distritos(request):
    provincia_id = request.GET.get('provincia_id')
    distritos = Distrito.objects.filter(id_provincia=provincia_id).values('id_distrito', 'nombre')
    return JsonResponse(list(distritos), safe=False)


def cargar_comunidades(request):
    distrito_id = request.GET.get('distrito_id')
    
    comunidades = Comunidad.objects.filter(id_distrito=distrito_id).values('id_comunidad', 'nombre')
    return JsonResponse(list(comunidades), safe=False)



#----------SECCION DE TRABAJOS GUARDADOS----------
@login_required
def dashboard_trabajador(request):
    usuario = request.user.perfil
    return render(request, 'trabajos/dashboard_trabajador.html', {'usuario': usuario})


def guardar_trabajo(request, tipo_oferta, oferta_id):
    if not hasattr(request.user, 'perfil'):
        messages.error(request, "Tu perfil de usuario no está completo.")
        return redirect('usuarios:login')

    usuario = request.user.perfil  # Ahora es instancia de tu modelo Usuario

    # Solo usuarios 'buscar-trabajo' o 'ambos' pueden guardar trabajos
    if usuario.tipo_usuario not in ['buscar-trabajo', 'ambos']:
        messages.error(request, "No tienes permiso para guardar trabajos.")
        return redirect('usuarios:login')

    # Determinar el modelo de la oferta según tipo
    if tipo_oferta == 'usuario':
        oferta_model = OfertaUsuario
    elif tipo_oferta == 'empresa':
        oferta_model = OfertaEmpresa
    else:
        messages.error(request, "Tipo de oferta no válido.")
        return redirect('usuarios:login')

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

    return redirect('trabajos:dashboard_trabajador')

@login_required
def trabajos_guardados(request):
    usuario = request.user.perfil   # Ahora es instancia de tu modelo Usuario
    trabajos_guardados = GuardarTrabajo.objects.filter(usuario=usuario).order_by('-fecha_guardado')
    return render(request, 'trabajos/trabajos_guardados.html', {'trabajos': trabajos_guardados})


@login_required
def trabajos_guardados_ajax(request):
    usuario = request.user.perfil
    trabajos_guardados = GuardarTrabajo.objects.filter(usuario=usuario).order_by('-fecha_guardado')

    html = render_to_string('trabajos/trabajos_guardados.html', {
        'trabajos': trabajos_guardados
    }, request=request)

    return JsonResponse({'html': html})







# views.py

@login_required
def quitar_guardado(request, id=None):  # id ya no es necesario en este enfoque
    if request.method != "POST":
        return redirect('trabajos:dashboard_trabajador')

    content_type_id = request.POST.get("content_type_id")
    object_id = request.POST.get("object_id")

    if not content_type_id or not object_id:
        return redirect('trabajos:dashboard_trabajador')

    try:
        content_type = ContentType.objects.get(id=content_type_id)
        model_class = content_type.model_class()
        oferta = model_class.objects.get(id=object_id)
    except Exception:
        return redirect('trabajos:dashboard_trabajador')

    usuario = get_object_or_404(Usuario, pk=request.user.pk)

    GuardarTrabajo.objects.filter(
        usuario=usuario,
        content_type=content_type,
        object_id=oferta.id
    ).delete()

    return redirect('trabajos:dashboard_trabajador')