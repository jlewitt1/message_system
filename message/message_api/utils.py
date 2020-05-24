from message_api.serializers import MessagesSerializer
from message_api.models import Messages


def handle_all_messages_queried(all_messages):
    """prepares messages for sending back to client"""
    serializer = MessagesSerializer(all_messages, many=True)
    res = [dict(_) for _ in serializer.data]
    all_messages.update(message_read=True)  # mark all messages retrieved as being read

    return res


def delete_message_for_given_receiver(receiver):
    try:
        res = Messages.objects.filter(receiver=receiver).latest('creation_date').delete()
        return res
    except Messages.DoesNotExist as e:
        return None
