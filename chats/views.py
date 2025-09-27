from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max
from .models import Chat, Mensaje
from .forms import MensajeForm, EditarMensajeForm
from django.utils import timezone
from usuarios.models import Usuario
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.timezone import now
from django.db import models


@login_required
def lista_chats(request):
    # Obtener el usuario personalizado usando el related_name 'perfil'
    try:
        usuario_actual = request.user.perfil
    except Usuario.DoesNotExist:
        return redirect('usuarios:perfil')
    
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
        # Buscar si existe un chat con este usuario
        chat_existente = Chat.objects.filter(
            (Q(usuario_1=usuario_actual) & Q(usuario_2=usuario)) |
            (Q(usuario_1=usuario) & Q(usuario_2=usuario_actual))
        ).first()
        
        # Obtener el último mensaje si existe el chat
        ultimo_mensaje = None
        fecha_ultimo_mensaje = None
        
        if chat_existente:
            ultimo_mensaje_obj = Mensaje.objects.filter(
                id_chat=chat_existente
            ).order_by('-fecha_envio').first()
            
            if ultimo_mensaje_obj:
                ultimo_mensaje = ultimo_mensaje_obj.contenido
                fecha_ultimo_mensaje = ultimo_mensaje_obj.fecha_envio
        
        # Obtener foto del perfil del usuario
        try:
            perfil_usuario = usuario.profile
            foto_url = perfil_usuario.foto_url.url if perfil_usuario.foto_url else ''
        except:
            foto_url = ''
        
        usuarios_con_chat.append({
            'usuario': usuario,
            'chat': chat_existente,
            'ultimo_mensaje': ultimo_mensaje,
            'fecha_ultimo_mensaje': fecha_ultimo_mensaje,
            'foto_url': foto_url,
            'nombre_completo': f"{usuario.nombres} {usuario.apellidos}" if usuario.nombres and usuario.apellidos else usuario.username
        })
    
    # Ordenar: primero por fecha de último mensaje (más reciente primero), luego alfabéticamente
    usuarios_con_chat.sort(key=lambda x: (
        x['fecha_ultimo_mensaje'] is None,  # Los sin mensaje van al final
        -(x['fecha_ultimo_mensaje'].timestamp() if x['fecha_ultimo_mensaje'] else 0),  # Más reciente primero
        x['nombre_completo'].lower()  # Alfabéticamente
    ))
    
    return render(request, 'chats/lista_chats.html', {
        'usuarios_con_chat': usuarios_con_chat,
        'usuario_actual': usuario_actual,
        'search_query': search_query
    })

@login_required
def ver_chat(request, usuario_id):
    try:
        usuario_actual = request.user.perfil
    except Usuario.DoesNotExist:
        return redirect('usuarios:perfil')
    
    otro_usuario = get_object_or_404(Usuario, id_usuario=usuario_id)

    # Buscar chat existente sin importar el orden de los usuarios
    chat = Chat.objects.filter(
        models.Q(usuario_1=usuario_actual, usuario_2=otro_usuario) |
        models.Q(usuario_1=otro_usuario, usuario_2=usuario_actual)
    ).first()

    # Si no existe, crear uno nuevo
    if not chat:
        chat = Chat.objects.create(
            usuario_1=usuario_actual,
            usuario_2=otro_usuario,
            fecha_creacion=now()
        )

    # Procesar formulario si es POST
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.id_chat = chat
            mensaje.remitente = usuario_actual
            mensaje.fecha_envio = timezone.now()
            mensaje.save()
            return redirect('chats:ver_chat', usuario_id=otro_usuario.id_usuario)
    else:
        form = MensajeForm()
    
    # Obtener mensajes del chat
    mensajes = Mensaje.objects.filter(id_chat=chat).order_by('fecha_envio')
    
    # Obtener foto del otro usuario
    try:
        perfil_otro_usuario = otro_usuario.profile
        foto_otro_usuario = perfil_otro_usuario.foto_url.url if perfil_otro_usuario.foto_url else ''
    except:
        foto_otro_usuario = ''
    
    return render(request, 'chats/ver_chat.html', {
        'chat': chat,
        'mensajes': mensajes,
        'form': form,
        'otro_usuario': otro_usuario,
        'foto_otro_usuario': foto_otro_usuario,
        'nombre_otro_usuario': f"{otro_usuario.nombres} {otro_usuario.apellidos}" if otro_usuario.nombres and otro_usuario.apellidos else otro_usuario.username
    })

@login_required
@require_POST
def editar_mensaje(request, mensaje_id):
    try:
        usuario_actual = request.user.perfil
    except Usuario.DoesNotExist:
        return redirect('usuarios:perfil')
    
    mensaje = get_object_or_404(Mensaje, id_mensaje=mensaje_id, remitente=usuario_actual)
    
    if request.method == 'POST':
        form = EditarMensajeForm(request.POST, instance=mensaje)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.editado = True
            mensaje.save()
            
            # Obtener el chat para redireccionar
            chat = mensaje.id_chat
            otro_usuario = chat.usuario_2 if chat.usuario_1 == usuario_actual else chat.usuario_1
            return redirect('chats:ver_chat', usuario_id=otro_usuario.id_usuario)
    
    return redirect('chats:lista_chats')

@login_required
@require_POST
def eliminar_mensaje(request, mensaje_id):
    try:
        usuario_actual = request.user.perfil
    except Usuario.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=400)
    
    try:
        mensaje = get_object_or_404(Mensaje, id_mensaje=mensaje_id, remitente=usuario_actual)
        mensaje.eliminado = True
        mensaje.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def ver_chat_por_id(request, chat_id):
    """Vista para abrir un chat específico por ID (usado desde dashboard)"""
    try:
        usuario_actual = request.user.perfil
    except Usuario.DoesNotExist:
        return redirect('usuarios:perfil')
    
    # Obtener el chat específico
    chat = get_object_or_404(Chat, id_chat=chat_id)
    
    # Verificar que el usuario actual participa en este chat
    if chat.usuario_1.id_usuario != usuario_actual.id_usuario and chat.usuario_2.id_usuario != usuario_actual.id_usuario:
        return redirect('chats:lista_chats')
    
    # Determinar el otro usuario
    otro_usuario = chat.usuario_2 if chat.usuario_1.id_usuario == usuario_actual.id_usuario else chat.usuario_1
    
    # Marcar como leídos todos los mensajes que no fueron enviados por el usuario actual
    mensajes_no_leidos = Mensaje.objects.filter(
        id_chat=chat,
        eliminado=False,
        leido=False
    ).exclude(remitente=usuario_actual)
    
    mensajes_no_leidos.update(leido=True)

    # Procesar formulario si es POST
    if request.method == 'POST':
        form = MensajeForm(request.POST)
        if form.is_valid():
            mensaje = form.save(commit=False)
            mensaje.id_chat = chat
            mensaje.remitente = usuario_actual
            mensaje.fecha_envio = timezone.now()
            mensaje.save()
            return redirect('chats:ver_chat_por_id', chat_id=chat.id_chat)
    else:
        form = MensajeForm()
    
    # Obtener mensajes del chat ordenados por fecha (solo los no eliminados)
    mensajes = Mensaje.objects.filter(id_chat=chat, eliminado=False).order_by('fecha_envio')
    
    # Obtener foto del otro usuario usando la relación correcta
    try:
        from usuarios.models import Profile
        perfil_otro_usuario = Profile.objects.get(id_usuario=otro_usuario)
        foto_otro_usuario = perfil_otro_usuario.foto_url.url if perfil_otro_usuario.foto_url else None
    except Profile.DoesNotExist:
        foto_otro_usuario = None
    
    return render(request, 'chats/ver_chat.html', {
        'chat': chat,
        'mensajes': mensajes,
        'form': form,
        'otro_usuario': otro_usuario,
        'foto_otro_usuario': foto_otro_usuario,
        'nombre_otro_usuario': f"{otro_usuario.nombres} {otro_usuario.apellidos}" if otro_usuario.nombres and otro_usuario.apellidos else otro_usuario.user.username
    })