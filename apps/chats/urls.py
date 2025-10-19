from django.urls import path
from . import views

app_name = 'chats'

urlpatterns = [
    # Lista de chats
    path('', views.lista_chats, name='lista_chats'),
    
    # Ver chat con un usuario específico
    path('con/<int:usuario_id>/', views.ver_chat, name='ver_chat'),
    
    # Ver chat por ID (usado desde dashboard)
    path('chat/<int:chat_id>/', views.ver_chat_por_id, name='ver_chat_por_id'),
    
    # Editar mensaje
    path('mensaje/editar/<int:mensaje_id>/', views.editar_mensaje, name='editar_mensaje'),
    
    # Eliminar mensaje
    path('mensaje/eliminar/<int:mensaje_id>/', views.eliminar_mensaje, name='eliminar_mensaje'),
]