from rest_framework import serializers
from message_api.models import Messages


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ('sender', 'receiver', 'message', 'subject', 'creation_date', 'message_read')
