from rest_framework import serializers
from django.contrib.auth.models import User
from message_api.models import Messages


class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = ('sender', 'receiver', 'message', 'subject', 'creation_date')
