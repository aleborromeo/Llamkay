from django.db.models import Q
from .models import Conversacion, Mensaje
from googletrans import Translator
translator = Translator()

def obtener_o_crear_chat(usuario_1, usuario_2):
    """
    Obtiene una conversación existente entre dos usuarios o la crea si no existe.
    """
    conversacion = Conversacion.objects.filter(
        Q(id_usuario_1=usuario_1, id_usuario_2=usuario_2) |
        Q(id_usuario_1=usuario_2, id_usuario_2=usuario_1)
    ).first()

    if not conversacion:
        # Normalizamos el orden para respetar el unique_together
        if usuario_1.id_usuario < usuario_2.id_usuario:
            conversacion = Conversacion.objects.create(
                id_usuario_1=usuario_1,
                id_usuario_2=usuario_2
            )
        else:
            conversacion = Conversacion.objects.create(
                id_usuario_1=usuario_2,
                id_usuario_2=usuario_1
            )

    return conversacion


def contar_mensajes_no_leidos(usuario):
    """
    Cuenta todos los mensajes no leídos para un usuario.
    """
    conversaciones = Conversacion.objects.filter(
        Q(id_usuario_1=usuario) | Q(id_usuario_2=usuario)
    )

    return Mensaje.objects.filter(
        id_conversacion__in=conversaciones,
        eliminado=False,
        leido=False
    ).exclude(id_remitente=usuario).count()


def marcar_mensajes_como_leidos(conversacion, usuario_actual):
    """
    Marca todos los mensajes de una conversación como leídos para el usuario actual.
    """
    Mensaje.objects.filter(
        id_conversacion=conversacion,
        eliminado=False,
        leido=False
    ).exclude(id_remitente=usuario_actual).update(leido=True)


def obtener_chats_recientes(usuario, limite=10):
    """
    Obtiene las conversaciones más recientes de un usuario.
    """
    conversaciones = Conversacion.objects.filter(
        Q(id_usuario_1=usuario) | Q(id_usuario_2=usuario)
    ).order_by('-ultimo_mensaje_at', '-created_at')[:limite]

    return conversaciones

def traducir_texto(texto, idioma_destino='en'):
    """
    Traduce un texto al idioma_destino usando googletrans.
    Devuelve (texto_traducido, idioma_origen).
    """
    if not texto:
        return '', 'auto'

    resultado = translator.translate(texto, dest=idioma_destino)
    return resultado.text, resultado.src

