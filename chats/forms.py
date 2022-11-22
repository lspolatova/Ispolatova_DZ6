from django import forms
from chats.models import Chat, Messages


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ('title', 'description', 'author', 'members', 'category', 'channel')


class MessageForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ('chat', 'sender', 'content', 'date_create', 'is_read', 'files')


class MessageIdForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ('sender', 'content', 'date_create', 'is_read', 'files')


class IdForm(forms.Form):
    id_chat = forms.CharField(label='id_chat')
    id_user = forms.CharField(label='id_user')
