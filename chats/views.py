from django.http import JsonResponse
from django.shortcuts import render
from chats.forms import ChatForm, MessageForm, IdForm, MessageIdForm
from chats.models import Chat, Messages
from users.models import User
from django.views.decorators.http import require_GET
from django.shortcuts import get_object_or_404


def form(form_input):
    """
    forms for tests
    """
    def inner_decorator(func):
        def inner_function(request, id_input=None):
            form_data = form_input(request.POST)
            if request.method == 'POST':
                if form_data.is_valid():
                    data = form_data.cleaned_data
                    if id_input:
                        return func(request, id_input, data)
                    return func(request, data)
                return JsonResponse({'chat': 'Form invalid!', 'errors': form_data.errors})
            return render(request, 'chats/create_form.html', {'form': form_data,
                                                              'url_var': func.__name__,
                                                              "id": id_input})
        return inner_function
    return inner_decorator


@form(ChatForm)
def add_chat(request, data):
    """
    create chat
    """
    members = data.pop('members')
    chat = Chat.objects.create(**data)
    chat.members.set(members)
    chat.save()
    return JsonResponse({'add_chat': 'Successfully added!'})


@form(ChatForm)
def update_chat(request, id_input, data):
    """
    edit chat by id
    """
    members = data.pop('members')
    chat = Chat.objects.filter(id=id_input)
    if chat:
        chat.update(**data)
        chat.last().members.set(members)
        chat.last().save()
        return JsonResponse({'update_chat': 'Successfully'})
    return JsonResponse({'update_chat': 'chat does not exist'}, status=400)


@form(IdForm)
def add_member(request, data):
    """
    add a participant to the chat by person id and chat id
    """
    id_user = data.pop('id_user')
    chat = get_object_or_404(Chat, id=data.pop('id_chat'))
    user = get_object_or_404(User, id=id_user)
    if chat.members.all().filter(id=id_user):
        return JsonResponse({'add_member': 'member already exists'})
    chat.members.add(user)
    return JsonResponse({'add_member': 'Successfully'})


@form(IdForm)
def delete_member(request, data):
    """
    remove a participant from the chat by person id and chat id
    """
    chat = get_object_or_404(Chat, id=data.pop('id_chat'))
    chat.members.remove(get_object_or_404(chat.members, id=data.pop('id_user')))
    return JsonResponse({'delete_member': 'Successfully'})


@require_GET
def delete_chat(request, id_chat):
    """
    delete chat by id
    """
    result = Chat.objects.filter(id=id_chat).delete()
    if result[0]:
        return JsonResponse(list(result), safe=False)
    # if zero objects have been deleted
    return JsonResponse({'delete_chat': 'chat does not exist'}, status=400)


@form(MessageIdForm)
def send_message(request, id_input, data):
    """
    send a message by chat id
    """
    chat = get_object_or_404(Chat, id=id_input)
    sender = data.pop('sender')
    if sender in chat.members.all():
        files = data.pop('files')
        message = Messages.objects.create(**data)
        message.files.set(files)
        message.chat = chat
        message.save()
        return JsonResponse({'send_message': 'Successfully'})
    return JsonResponse({'send_message': 'There is no such user in the chat'}, status=400)


@form(MessageForm)
def update_message(request, id_input, data):
    """
    edit a message by message id
    """
    message = Messages.objects.filter(id=id_input)
    if message:
        sender = data.pop('sender')
        chat = data.pop('chat')
        if sender in chat.members.all():
            files = data.pop('files')
            message.update(**data)
            message.files.set(files)
            message.save()
            return JsonResponse({'update_message': 'Successfully'})
        return JsonResponse({'update_message': 'There is no such user in the chat'}, status=400)
    return JsonResponse({'update_message': 'message does not exist'}, status=400)


@require_GET
def message_read(request, id_message):
    """
    mark a message as read by message id
    """
    message = get_object_or_404(Messages, id=id_message)
    message.is_read = True
    message.save()
    return JsonResponse({'message_read': 'Successfully'})


@require_GET
def delete_message(request, id_message):
    """
    delete a message by message id
    """
    result = Messages.objects.filter(id=id_message).delete()
    if result[0]:
        return JsonResponse(list(result), safe=False)
    # if zero objects have been deleted
    return JsonResponse({'delete_message': 'message does not exist'})


@require_GET
def chat_list(request):
    """
    get chat list
    """
    chat = list(Chat.objects.values('id', 'title'))
    return JsonResponse(chat, safe=False)


@require_GET
def get_message_chat(request, id_chat):
    """
    get a list of messages by chat id
    """
    message = list(get_object_or_404(Chat, id=id_chat).messages.all().values())
    return JsonResponse(message, safe=False)


@require_GET
def get_chat(request, id_chat):
    """
    get chat information by id
    """
    chat = list(Chat.objects.filter(id=id_chat).values())
    members = list(Chat.objects.filter(id=id_chat).values_list('members', flat=True))
    return JsonResponse({'chat': chat, 'members_id': members})
