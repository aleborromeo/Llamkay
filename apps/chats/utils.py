from django.db.models import Q
from .models import Chat, Mensaje


def obtener_o_crear_chat(usuario_1, usuario_2):
    """
    Obtiene un chat existente entre dos usuarios o lo crea si no existe.
    
    Args:
        usuario_1: Usuario actual
        usuario_2: Otro usuario
    
    Returns:
        Chat: Instancia del chat
    """
    chat = Chat.objects.filter(
        Q(usuario_1=usuario_1, usuario_2=usuario_2) |
        Q(usuario_1=usuario_2, usuario_2=usuario_1)
    ).first()
    
    if not chat:
        chat = Chat.objects.create(
            usuario_1=usuario_1,
            usuario_2=usuario_2
        )
    
    return chat


def contar_mensajes_no_leidos(usuario):
    """
    Cuenta todos los mensajes no leídos para un usuario.
    
    Args:
        usuario: Usuario para contar mensajes
    
    Returns:
        int: Cantidad de mensajes no leídos
    """
    # Obtener todos los chats donde participa el usuario
    chats = Chat.objects.filter(
        Q(usuario_1=usuario) | Q(usuario_2=usuario)
    )
    
    # Contar mensajes no leídos que no fueron enviados por el usuario
    return Mensaje.objects.filter(
        id_chat__in=chats,
        eliminado=False,
        leido=False
    ).exclude(remitente=usuario).count()


def marcar_mensajes_como_leidos(chat, usuario_actual):
    """
    Marca todos los mensajes de un chat como leídos para el usuario actual.
    
    Args:
        chat: Chat donde marcar mensajes
        usuario_actual: Usuario que está leyendo
    """
    Mensaje.objects.filter(
        id_chat=chat,
        eliminado=False,
        leido=False
    ).exclude(remitente=usuario_actual).update(leido=True)


def obtener_chats_recientes(usuario, limite=10):
    """
    Obtiene los chats más recientes de un usuario.
    
    Args:
        usuario: Usuario para obtener chats
        limite: Cantidad máxima de chats a retornar
    
    Returns:
        QuerySet: Chats ordenados por último mensaje
    """
    chats = Chat.objects.filter(
        Q(usuario_1=usuario) | Q(usuario_2=usuario)
    ).order_by('-fecha_creacion')[:limite]
    
    return chats