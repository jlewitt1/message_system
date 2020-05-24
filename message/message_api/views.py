import ast
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict
from message_api.models import Messages
from message_api.serializers import MessagesSerializer
from message_api.utils import handle_all_messages_queried, delete_message_for_given_receiver


@csrf_exempt
@api_view(['POST', 'GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def handle_given_message(request):
    """writes a new message / queries the most recent existing message / deletes a message for the given user"""
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
        try:  # read most recent message for specified receiver
            receiver = request.user.email
            message = Messages.objects.filter(receiver=receiver).latest('creation_date')
            res = model_to_dict(message, fields=[field.name for field in Messages._meta.fields[1:]])
            return Response(res, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if request.method == 'DELETE':
        user = request.user.email
        res = delete_message_for_given_receiver(user)
        if not res:
            return Response({"Error": f"Record for {user} does not exist"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(res, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def query_messages(request, get_all_messages):
    """gets multiple messages for given user (includes boolean param for querying only unread messages)"""
    if request.method == 'GET':
        user = request.user.email
        all_messages = {}
        try:
            query_all = ast.literal_eval(get_all_messages)
            if not query_all:  # if only searching for unread messages
                all_messages = Messages.objects.filter(receiver=user, message_read=query_all)
            if query_all:  # if querying all messages
                all_messages = Messages.objects.filter(receiver=user)
            if all_messages:
                res = handle_all_messages_queried(all_messages)
                return Response(res, status=status.HTTP_200_OK)
            else:
                return Response({"Error": f"No data found for {user} and get_all_messages {query_all}"},
                                status=status.HTTP_206_PARTIAL_CONTENT)
        except Exception as e:
            return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
