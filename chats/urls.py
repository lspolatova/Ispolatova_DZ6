from django.urls import path
from chats.views import ChatListAdd, ChatGetDeleteUpdate, MemberChat, MessageListAdd, MessageGetDeleteUpdate,\
    MessageRead

urlpatterns = [
    path('list_add/', ChatListAdd.as_view(), name='list_add'),
    path('get_delete_update/<int:pk>/', ChatGetDeleteUpdate.as_view(), name='get_delete_update'),
    path('add_delete_member/', MemberChat.as_view({'post': 'create', 'delete': 'destroy'}), name='add_delete_member'),
    path('message_list_add/', MessageListAdd.as_view(), name='message_list_add'),
    path('message_get_delete_update/<int:pk>/', MessageGetDeleteUpdate.as_view(), name='message_get_delete_update'),
    path('message_read/<int:pk>/', MessageRead.as_view({'put': 'partial_update'}), name='message_read'),
]
