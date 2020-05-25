from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from message_api.serializers import MessagesSerializer
from message_api.utils import get_all_messages_for_user, delete_message_for_given_user, read_single_message_for_user, \
    validate_user_type_for_deleting_message


@csrf_exempt
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def handle_given_message(request, message_id=''):
    """writes a new message with data provided or queries the most recent existing message or by id if provided"""
    if request.method == 'POST':
        all_data = request.data
        try:
            serializer = MessagesSerializer(data=all_data)
            if serializer.is_valid():
                serializer.save()
                return Response("Message recorded successfully", status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'GET':
        try:  # read message for specified receiver
            receiver = request.user.email
            message_data = read_single_message_for_user(receiver, message_id)
            return Response(message_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def query_messages(request, message_type=''):
    """gets multiple messages for given user (based on param for whether to query only unread messages)"""
    if request.method == 'GET':
        receiver = request.user.email
        query_all = True
        if message_type:  # if left empty query all
            if message_type.lower() == "unread":
                query_all = False
            else:
                return Response({"Error": f"Invalid url param {message_type}"},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        all_messages = get_all_messages_for_user(receiver, query_all)
        if all_messages:
            return Response(all_messages, status=status.HTTP_200_OK)
        return Response({"Error": f"No messages found for {receiver}"}, status=status.HTTP_206_PARTIAL_CONTENT)


@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_message(request, user_type='', message_id=''):
    """deletes given message for user by id if provided - otherwise delete most recent based on user type"""
    if request.method == 'DELETE':
        user = request.user.email
        valid_user_type = validate_user_type_for_deleting_message(user_type.lower())
        if not valid_user_type and not message_id:  # must provide either a valid user type or message_id
            return Response({"Error": f"Invalid url param"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        res = delete_message_for_given_user(user, valid_user_type, message_id)
        if not res:  # if error with querying table or record does not exist
            return Response({"Error": f"Failed to delete record for user {user}"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(f"Record for user {user} deleted successfully", status=status.HTTP_200_OK)
