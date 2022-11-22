from django.urls import path
from chats.views import add_chat, get_chat, \
    update_chat, update_message, delete_chat, delete_message, add_member, delete_member, \
    message_read, chat_list, get_message_chat, send_message

urlpatterns = [
    path('add_chat/', add_chat, name='add_chat'),
    path('get_chat/<int:id_chat>/', get_chat, name='get_chat'),
    path('update_chat/<int:id_input>/', update_chat, name='update_chat'),
    path('update_message/<int:id_input>/', update_message, name='update_message'),
    path('delete_chat/<int:id_chat>/', delete_chat, name='delete_chat'),
    path('delete_message/<int:id_message>/', delete_message, name='delete_message'),
    path('add_member', add_member, name='add_member'),
    path('delete_member', delete_member, name='delete_member'),
    path('message_read/<int:id_message>/', message_read, name='message_read'),
    path('chat_list', chat_list, name='chat_list'),
    path('get_message_chat/<int:id_chat>/', get_message_chat, name='get_message_chat'),
    path('send_message/<int:id_input>/', send_message, name='send_message'),
]
