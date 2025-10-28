"""
Vistas de Denuncias
SRP: Solo maneja la presentación de denuncias
DIP: Depende de DenunciaService (abstracción)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core.paginator import Paginator
import logging

from apps.users.models import Usuario
from apps.jobs.models import Contrato
from apps.chats.models import Mensaje
from ..services import DenunciaService
from ..models import Denuncia

logger = logging.getLogger(__name__)


@login_required
def listar_denuncias(request):
    """
    Lista todas las denuncias del usuario autenticado
    """
    try:
        # IMPORTAR Usuario
        from apps.users.models import Usuario
        
        # OBTENER el objeto Usuario (no User)
        try:
            usuario = Usuario.objects.get(user=request.user)
        except Usuario.DoesNotExist:
            messages.error(request, "No se encontró tu perfil de usuario.")
            return redirect('llamkay:dashboard')  # ← Usa dashboard, no 'home'

        # Servicio
        service = DenunciaService()
        denuncias = service.obtener_denuncias_usuario(usuario)  # ← Pasa 'usuario', no 'request.user'

        context = {
            'denuncias': denuncias,
            'count': len(denuncias),
        }
        return render(request, 'soporte/denuncias/lista.html', context)

    except Exception as e:
        logger.error(f"Error listando denuncias: {str(e)}", exc_info=True)
        messages.error(request, "Error al cargar tus denuncias.")
        return redirect('llamkay:dashboard')  # ← CORREGIDO


@login_required
@require_http_methods(["GET", "POST"])
def crear_denuncia(request):
    """
    Vista para crear una denuncia
    GET: Muestra el formulario
    POST: Crea la denuncia
    """
    if request.method == 'GET':
        # Obtener parámetros para pre-llenar el formulario
        id_denunciado = request.GET.get('usuario')
        id_contrato = request.GET.get('contrato')
        id_mensaje = request.GET.get('mensaje')
        
        context = {
            'motivos': Denuncia.MOTIVO_CHOICES,
            'id_denunciado': id_denunciado,
            'id_contrato': id_contrato,
            'id_mensaje': id_mensaje,
        }
        
        return render(request, 'soporte/denuncias/crear.html', context)
    
    # POST - Crear denuncia
    try:
        service = DenunciaService()
        
        # Obtener datos del formulario
        id_denunciado = request.POST.get('id_denunciado')
        motivo = request.POST.get('motivo')
        descripcion = request.POST.get('descripcion')
        evidencia_url = request.POST.get('evidencia_url')
        id_contrato = request.POST.get('id_contrato')
        id_mensaje = request.POST.get('id_mensaje')
        
        # Validaciones
        if not id_denunciado or not motivo or not descripcion:
            messages.error(request, 'Por favor completa todos los campos requeridos')
            return redirect('soporte:crear_denuncia')
        
        # Obtener objetos relacionados
        denunciado = get_object_or_404(Usuario, id_usuario=id_denunciado)
        
        contrato_obj = None
        if id_contrato:
            contrato_obj = get_object_or_404(Contrato, id_contrato=id_contrato)
        
        mensaje_obj = None
        if id_mensaje:
            mensaje_obj = get_object_or_404(Mensaje, id_mensaje=id_mensaje)
        
        # Crear denuncia
        result = service.crear_denuncia(
            id_reportante=request.user,
            id_denunciado=denunciado,
            motivo=motivo,
            descripcion=descripcion,
            id_contrato=contrato_obj,
            id_mensaje=mensaje_obj,
            evidencia_url=evidencia_url
        )
        
        if result['success']:
            messages.success(request, 'Denuncia creada exitosamente')
            return redirect('soporte:detalle_denuncia', id_denuncia=result['denuncia'].id_denuncia)
        else:
            messages.error(request, result['error'])
            return redirect('soporte:crear_denuncia')
        
    except Exception as e:
        logger.error(f"Error creando denuncia: {str(e)}")
        messages.error(request, f'Error al crear la denuncia: {str(e)}')
        return redirect('soporte:crear_denuncia')


@login_required
def detalle_denuncia(request, id_denuncia):
    """
    Vista para ver el detalle de una denuncia
    GET: Muestra los detalles de la denuncia
    POST: Actualizar estado (solo moderadores)
    """
    try:
        service = DenunciaService()
        denuncia = service.obtener_denuncia(id_denuncia)
        
        if not denuncia:
            messages.error(request, 'Denuncia no encontrada')
            return redirect('soporte:denuncias')
        
        # Verificar permisos
        es_moderador = request.user.is_staff or request.user.is_superuser
        es_reportante = denuncia.id_reportante.id_usuario == request.user.id_usuario
        
        if not (es_moderador or es_reportante):
            messages.error(request, 'No tienes permiso para ver esta denuncia')
            return redirect('soporte:denuncias')
        
        # POST - Actualizar estado (solo moderadores)
        if request.method == 'POST' and es_moderador:
            accion = request.POST.get('accion')
            
            if accion == 'asignar':
                result = service.asignar_moderador(id_denuncia, request.user)
            elif accion == 'resolver':
                resolucion = request.POST.get('resolucion')
                result = service.resolver_denuncia(id_denuncia, resolucion, request.user)
            elif accion == 'rechazar':
                motivo = request.POST.get('motivo_rechazo')
                result = service.rechazar_denuncia(id_denuncia, motivo, request.user)
            elif accion == 'cerrar':
                result = service.cerrar_denuncia(id_denuncia, request.user)
            else:
                messages.error(request, 'Acción no válida')
                return redirect('soporte:detalle_denuncia', id_denuncia=id_denuncia)
            
            if result['success']:
                messages.success(request, result['message'])
            else:
                messages.error(request, result['error'])
            
            return redirect('soporte:detalle_denuncia', id_denuncia=id_denuncia)
        
        # GET - Mostrar detalles
        context = {
            'denuncia': denuncia,
            'es_moderador': es_moderador,
            'es_reportante': es_reportante,
        }
        
        return render(request, 'soporte/denuncias/detalle.html', context)
        
    except Exception as e:
        logger.error(f"Error en detalle de denuncia: {str(e)}")
        messages.error(request, 'Error al cargar la denuncia')
        return redirect('soporte:denuncias')