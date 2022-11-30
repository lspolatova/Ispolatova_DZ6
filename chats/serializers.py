from rest_framework import serializers
from chats.models import Chat, Messages


class ChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = '__all__'


class MembersSerializer(serializers.ModelSerializer):

    class Meta:
        model = Chat
        fields = ['members']


class MessageSerializer_without_chat(serializers.ModelSerializer):

    class Meta:
        model = Messages
        fields = ['id', 'sender', 'content', 'date_create', 'is_read', 'files']


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Messages
        fields = '__all__'
