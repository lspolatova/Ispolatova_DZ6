from django.http import JsonResponse
from django.shortcuts import render
from chats.models import Chat, Messages
from users.models import User
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import viewsets
from chats.serializers import ChatSerializer, MessageSerializer, MessageSerializer_without_chat
from django.core.exceptions import ValidationError
from rest_framework.filters import BaseFilterBackend
from chats.tasks import send_email, task_publish
from django.views.decorators.csrf import ensure_csrf_cookie


class ChatFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        queryset = queryset.filter(members=request.user)
        return queryset


class ChatListAdd(ListCreateAPIView):
    """
    create chat, get chat list
    """
    filter_backends = (ChatFilter,)

    def perform_create(self, serializer):
        members_serializer = self.request.data.getlist('members')
        members_serializer.append(self.request.user.id)
        return serializer.save(author=self.request.user, members=members_serializer)
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()


class ChatGetDeleteUpdate(RetrieveUpdateDestroyAPIView):
    """
    edit chat by id, delete chat by id, get chat information by id
    """
    filter_backends = (ChatFilter,)

    def perform_destroy(self, serializer):
        if self.request.user != get_object_or_404(Chat, id=self.kwargs['pk']).author:
            raise ValidationError('For this action, the user must be the author')
        return serializer.delete()

    def perform_update(self, serializer):
        if self.request.user != get_object_or_404(Chat, id=self.kwargs['pk']).author:
            raise ValidationError('For this action, the user must be the author')
        return serializer.save()
    serializer_class = ChatSerializer
    queryset = Chat.objects.all()


class MemberChat(viewsets.ViewSet):
    @staticmethod
    def create(request):
        """
        add a participant to the chat by person id and chat id
        """
        chat = get_object_or_404(Chat, id=request.query_params.get('id_chat'))
        if request.user != chat.author:
            raise ValidationError('For this action, the user must be the author')
        user = get_object_or_404(User, id=request.query_params.get('id_user'))
        if chat.members.all().filter(id=request.query_params.get('id_user')):
            raise ValidationError('member already exists')
        chat.members.add(user)
        send_email.delay([chat.author.email], chat.id)
        return JsonResponse({'add_member': 'Successfully'})

    @staticmethod
    def destroy(request):
        """
        remove a participant from the chat by person id and chat id
        """
        chat = get_object_or_404(Chat, id=request.query_params.get('id_chat'))
        if request.user != chat.author:
            raise ValidationError('For this action, the user must be the author')
        chat.members.remove(get_object_or_404(chat.members, id=request.query_params.get('id_user')))
        return JsonResponse({'delete_member': 'Successfully'})


class MessageChatFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        chat = request.GET.get('id_chat')
        if not get_object_or_404(Chat, id=chat).members.filter(id=request.user.id):
            raise ValidationError('the user is not in the chat')
        queryset = queryset.filter(chat__id=chat)
        return queryset


class MessageListAdd(ListCreateAPIView):
    """
    send a message by chat id, get a list of messages by chat id
    """
    serializer_class = MessageSerializer_without_chat
    #filter_backends = (MessageChatFilter, )

    def perform_create(self, serializer):
        chat = get_object_or_404(Chat, id=self.request.query_params.get('id_chat'))
        sender = get_object_or_404(User, id=1)
        if sender in chat.members.all():
            print(self.request.data.get('content'))
            task_publish.delay(self.request.data.get('content'))
            return serializer.save(chat=chat, sender=sender)
        raise ValidationError('There is no such user in the chat')
    queryset = Messages.objects.all()


class MessageUserFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(chat__members=request.user)


class MessageGetDeleteUpdate(RetrieveUpdateDestroyAPIView):
    """
    edit a message by message id, delete a message by message id
    """
    serializer_class = MessageSerializer
    filter_backends = (MessageUserFilter,)

    def perform_update(self, serializer):
        sender = get_object_or_404(Messages, id=self.kwargs['pk']).sender
        if sender != self.request.user:
            raise ValidationError('the user is not the sender')
        chat = get_object_or_404(Chat, id=self.request.data.get("chat"))
        if sender in chat.members.all():
            return serializer.save(chat=chat, sender=sender)
        raise ValidationError('There is no such user in the chat')

    def perform_destroy(self, serializer):
        sender = get_object_or_404(Messages, id=self.kwargs['pk']).sender
        if sender != self.request.user:
            raise ValidationError('the user is not the sender')
        return serializer.delete()
    queryset = Messages.objects.all()


class MessageRead(viewsets.ViewSet):
    @staticmethod
    def partial_update(request, pk):
        """
        mark a message as read by message id
        """
        message = get_object_or_404(Messages, id=pk)
        if not (message.chat.members.filter(id=request.user.id)) or request.user == message.sender:
            raise ValidationError('the message cannot be read by this user')
        message.is_read = True
        message.save()
        return JsonResponse({'message_read': 'Successfully'})


def login(request):
    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')
