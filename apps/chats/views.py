from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages

from .models import Conversacion, Mensaje
from .forms import MensajeForm, EditarMensajeForm
from apps.users.models import Usuario, Profile


@login_required
def lista_chats(request):
    """Vista para mostrar la lista de chats del usuario"""
    try:
        usuario_actual = request.user.perfil
    except Usuario.DoesNotExist:
        messages.error(request, 'Debes completar tu perfil primero.')
        return redirect('users:perfil')
    
    # Obtener término de búsqueda
    search_query = request.GET.get('search', '').strip()
    
    # Obtener todos los usuarios registrados excepto el usuario actual
    todos_usuarios = Usuario.objects.exclude(id_usuario=usuario_actual.id_usuario)
    
    # Filtrar por búsqueda si hay término de búsqueda
    if search_query:
        todos_usuarios = todos_usuarios.filter(
            Q(nombres__icontains=search_query) |
            Q(apellidos__icontains=search_query) |
            Q(username__icontains=search_query)
        )
    
    # Crear una lista de usuarios con información de chat
    usuarios_con_chat = []
    
    for usuario in todos_usuarios:
        # Buscar si existe una conversación con este usuario
        conversacion_existente = Conversacion.objects.filter(
            (Q(id_usuario_1=usuario_actual) & Q(id_usuario_2=usuario)) |
            (Q(id_usuario_1=usuario) & Q(id_usuario_2=usuario_actual))
        ).first()
        
        # Obtener el último mensaje si existe la conversación
        ultimo_mensaje = None
        fecha_ultimo_mensaje = None
        mensajes_no_leidos = 0
        
        if conversacion_existente:
            ultimo_mensaje_obj = conversacion_existente.mensajes.filter(
                eliminado=False
            ).order_by('-fecha_envio').first()
            
            if ultimo_mensaje_obj:
                ultimo_mensaje = ultimo_mensaje_obj.contenido
                fecha_ultimo_mensaje = ultimo_mensaje_obj.fecha_envio
            
            # Contar mensajes no leídos
            mensajes_no_leidos = Mensaje.objects.filter(
                id_conversacion=conversacion_existente,
                eliminado=False,
                leido=False
            ).exclude(id_remitente=usuario_actual).count()
        
        # Obtener foto del perfil del usuario
        try:
            perfil_usuario = usuario.profile
            foto_url = perfil_usuario.foto_url.url if perfil_usuario.foto_url else None
        except Profile.DoesNotExist:
            foto_url = None
        
        usuarios_con_chat.append({
            'usuario': usuario,
            'conversacion': conversacion_existente,
            'ultimo_mensaje': ultimo_mensaje,
            'fecha_ultimo_mensaje': fecha_ultimo_mensaje,
            'foto_url': foto_url,
            'mensajes_no_leidos': mensajes_no_leidos,
            'nombre_completo': f"{usuario.nombres} {usuario.apellidos}" if usuario.nombres and usuario.apellidos else usuario.username
        })
    
    # Ordenar: primero por fecha de último mensaje (más reciente primero), luego alfabéticamente
    usuarios_con_chat.sort(key=lambda x: (
        x['fecha_ultimo_mensaje'] is None,
        -(x['fecha_ultimo_mensaje'].timestamp() if x['fecha_ultimo_mensaje'] else 0),
        x['nombre_completo'].lower()
    ))
    
    return render(request, 'chats/lista_chats.html', {
        'usuarios_con_chat': usuarios_con_chat,
        'usuario_actual': usuario_actual,
        'search_query': search_query
    })


@login_required
def ver_chat(request, usuario_id):
    """Vista para ver o crear un chat con un usuario específico"""
    try:
        usuario_actual = request.user.perfil
    except Usuario.DoesNotExist:
        messages.error(request, 'Debes completar tu perfil primero.')
        return redirect('users:perfil')
    
    otro_usuario = get_object_or_404(Usuario, id_usuario=usuario_id)

    # Verificar que no sea el mismo usuario
    if otro_usuario.id_usuario == usuario_actual.id_usuario:
        messages.warning(request, 'No puedes chatear contigo mismo.')
        return redirect('chats:lista_chats')

    # Buscar conversación existente sin importar el orden de los usuarios
    conversacion = Conversacion.objects.filter(
        Q(id_usuario_1=usuario_actual, id_usuario_2=otro_usuario) |
        Q(id_usuario_1=otro_usuario, id_usuario_2=usuario_actual)
    ).first()

    # Si no existe, crear una nueva
    if not conversacion:
        # Asegurar que id_usuario_1 < id_usuario_2 (según constraint del SQL)
        if usuario_actual.id_usuario < otro_usuario.id_usuario:
            conversacion = Conversacion.objects.create(
                id_usuario_1=usuario_actual,
                id_usuario_2=otro_usuario
            )
        else:
            conversacion = Conversacion.objects.create(
                id_usuario_1=otro_usuario,
                id_usuario_2=usuario_actual
            )

    # Marcar mensajes como leídos
    Mensaje.objects.filter(
        id_conversacion=conversacion,
        eliminado=False,
        leido=False
    ).exclude(id_remitente=usuario_actual).update(
        leido=True,
        fecha_leido=timezone.now()
    )

    # Procesar formulario si es POST
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.id_conversacion = conversacion
            mensaje.id_remitente = usuario_actual
            mensaje.save()
            
            # Actualizar último mensaje de la conversación
            conversacion.ultimo_mensaje_at = timezone.now()
            conversacion.save(update_fields=['ultimo_mensaje_at'])
            
            messages.success(request, 'Mensaje enviado correctamente.')
            return redirect('chats:ver_chat', usuario_id=otro_usuario.id_usuario)
    else:
        form = MensajeForm()
    
    # Obtener mensajes de la conversación (solo no eliminados)
    mensajes = Mensaje.objects.filter(
        id_conversacion=conversacion, 
        eliminado=False
    ).select_related('id_remitente').order_by('fecha_envio')
    
    # Obtener foto del otro usuario
    try:
        perfil_otro_usuario = otro_usuario.profile
        foto_otro_usuario = perfil_otro_usuario.foto_url.url if perfil_otro_usuario.foto_url else None
    except Profile.DoesNotExist:
        foto_otro_usuario = None
    
    return render(request, 'chats/ver_chat.html', {
        'conversacion': conversacion,
        'mensajes': mensajes,
        'form': form,
        'otro_usuario': otro_usuario,
        'foto_otro_usuario': foto_otro_usuario,
        'nombre_otro_usuario': f"{otro_usuario.nombres} {otro_usuario.apellidos}" if otro_usuario.nombres and otro_usuario.apellidos else otro_usuario.username,
        'usuario_actual': usuario_actual
    })


@login_required
def ver_chat_por_id(request, chat_id):
    """Vista para abrir un chat específico por ID (usado desde dashboard)"""
    try:
        usuario_actual = request.user.perfil
    except Usuario.DoesNotExist:
        messages.error(request, 'Debes completar tu perfil primero.')
        return redirect('users:perfil')
    
    # Obtener la conversación específica
    conversacion = get_object_or_404(Conversacion, id_conversacion=chat_id)
    
    # Verificar que el usuario actual participa en esta conversación
    if conversacion.id_usuario_1.id_usuario != usuario_actual.id_usuario and conversacion.id_usuario_2.id_usuario != usuario_actual.id_usuario:
        messages.error(request, 'No tienes permiso para ver esta conversación.')
        return redirect('chats:lista_chats')
    
    # Determinar el otro usuario usando el método del modelo
    otro_usuario = conversacion.obtener_otro_usuario(usuario_actual)
    
    # Marcar como leídos todos los mensajes que no fueron enviados por el usuario actual
    Mensaje.objects.filter(
        id_conversacion=conversacion,
        eliminado=False,
        leido=False
    ).exclude(id_remitente=usuario_actual).update(
        leido=True,
        fecha_leido=timezone.now()
    )

    # Procesar formulario si es POST
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.id_conversacion = conversacion
            mensaje.id_remitente = usuario_actual
            mensaje.save()
            
            # Actualizar último mensaje de la conversación
            conversacion.ultimo_mensaje_at = timezone.now()
            conversacion.save(update_fields=['ultimo_mensaje_at'])
            
            messages.success(request, 'Mensaje enviado correctamente.')
            return redirect('chats:ver_chat_por_id', chat_id=conversacion.id_conversacion)
    else:
        form = MensajeForm()
    
    # Obtener mensajes de la conversación ordenados por fecha (solo los no eliminados)
    mensajes = Mensaje.objects.filter(
        id_conversacion=conversacion, 
        eliminado=False
    ).select_related('id_remitente').order_by('fecha_envio')
    
    # Obtener foto del otro usuario
    try:
        perfil_otro_usuario = Profile.objects.get(id_usuario=otro_usuario)
        foto_otro_usuario = perfil_otro_usuario.foto_url.url if perfil_otro_usuario.foto_url else None
    except Profile.DoesNotExist:
        foto_otro_usuario = None
    
    return render(request, 'chats/ver_chat.html', {
        'conversacion': conversacion,
        'mensajes': mensajes,
        'form': form,
        'otro_usuario': otro_usuario,
        'foto_otro_usuario': foto_otro_usuario,
        'nombre_otro_usuario': f"{otro_usuario.nombres} {otro_usuario.apellidos}" if otro_usuario.nombres and otro_usuario.apellidos else otro_usuario.username,
        'usuario_actual': usuario_actual
    })


@login_required
@require_POST
def editar_mensaje(request, mensaje_id):
    """Vista para editar un mensaje existente"""
    try:
        usuario_actual = request.user.perfil
    except Usuario.DoesNotExist:
        messages.error(request, 'Debes completar tu perfil primero.')
        return redirect('users:perfil')
    
    mensaje = get_object_or_404(Mensaje, id_mensaje=mensaje_id, id_remitente=usuario_actual)
    
    form = EditarMensajeForm(request.POST, instance=mensaje)
    if form.is_valid():
        mensaje = form.save(commit=False)
        mensaje.editado = True
        mensaje.save()
        messages.success(request, 'Mensaje editado correctamente.')
        
        # Obtener la conversación para redireccionar
        conversacion = mensaje.id_conversacion
        otro_usuario = conversacion.obtener_otro_usuario(usuario_actual)
        return redirect('chats:ver_chat', usuario_id=otro_usuario.id_usuario)
    else:
        messages.error(request, 'Error al editar el mensaje.')
    
    return redirect('chats:lista_chats')


@login_required
@require_POST
def eliminar_mensaje(request, mensaje_id):
    """Vista para eliminar (marcar como eliminado) un mensaje"""
    try:
        usuario_actual = request.user.perfil
    except Usuario.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=400)
    
    try:
        mensaje = get_object_or_404(Mensaje, id_mensaje=mensaje_id, id_remitente=usuario_actual)
        
        mensaje.eliminado = True
        mensaje.save(update_fields=['eliminado'])
        return JsonResponse({'success': True, 'message': 'Mensaje eliminado correctamente'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)