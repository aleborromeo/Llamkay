from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'chats'

urlpatterns = [
    path('', views.lista_chats, name='lista_chats'),
    path('con/<int:usuario_id>/', views.ver_chat, name='ver_chat'),
    path('chat/<int:chat_id>/', views.ver_chat_por_id, name='ver_chat_por_id'),
    path('editar/<int:mensaje_id>/', views.editar_mensaje, name='editar_mensaje'),
    path('eliminar/<int:mensaje_id>/', views.eliminar_mensaje, name='eliminar_mensaje'),
]