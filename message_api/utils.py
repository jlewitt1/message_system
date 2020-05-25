from message_api.serializers import MessagesSerializer
from message_api.models import Messages
from django.forms.models import model_to_dict


def handle_all_messages_queried(all_messages):
    """prepares all messages for sending back to client"""
    serializer = MessagesSerializer(all_messages, many=True)
    all_data = [dict(_) for _ in serializer.data]
    all_messages.update(message_read=True)  # mark all messages retrieved as being read

    return all_data


def handle_delete_query_response(res):
    if not res or res[0] == 0:  # if no record to delete
        return False
    return True


def read_single_message_for_user(receiver, message_id):
    """reads a given message for a specific user (according to whether a message_id has been provided)"""
    if message_id:  # read specified message with provided id
        message = Messages.objects.get(pk=message_id)
    else:
        message = Messages.objects.filter(receiver=receiver).latest('creation_date')
    # mark message as read after querying
    message.message_read = True
    message.save()
    message_data = model_to_dict(message, fields=[field.name for field in Messages._meta.fields[1:]])

    return message_data


def get_all_messages_for_user(receiver, query_all):
    """queries table for all messages for a given user including flag for whether to query only unread messages"""
    all_messages = None
    if not query_all:  # if only searching for unread messages
        all_messages = Messages.objects.filter(receiver=receiver, message_read=query_all)
    if query_all:  # if querying all messages (regardless of message_read status)
        all_messages = Messages.objects.filter(receiver=receiver)
    if not all_messages:  # if no messages under given filter params
        return None
    res = handle_all_messages_queried(all_messages)
    return res


def delete_most_recent_message(user_type, user):
    try:
        if user_type == 'owner':  # delete the entire message
            query_res = Messages.objects.filter(sender=user).latest('creation_date').delete()
            return handle_delete_query_response(query_res)
        else:  # if receiver then do not delete message - just delete for recipient (set to empty string)
            latest_msg = Messages.objects.filter(receiver=user).latest('creation_date')
            latest_msg.receiver = ''
            latest_msg.save()
            return True
    except Messages.DoesNotExist:
        return False


def delete_message_for_given_user(user, user_type, message_id):
    """handles deletion of a given message based on whether user is owner or recipient (and whether id is provided)"""
    if message_id:  # if request to delete a specific message by id (regardless of whether user is owner / recipient)
        try:
            query_res = Messages.objects.filter(pk=message_id).delete()
            return handle_delete_query_response(query_res)
        except Messages.DoesNotExist:
            return False
    else:
        res = delete_most_recent_message(user_type, user)
        return res


def validate_user_type_for_deleting_message(user_type):
    if user_type == 'owner' or user_type == 'receiver':
        return user_type.lower()
