from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from message_api.models import Messages

from message_api.serializers import MessagesSerializer


@csrf_exempt
@api_view(['GET'])
def sanity_check(request):
    return Response(b'OK', status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['POST'])
def write_new_message(request):
    """handles writing a new message received (sender, receiver, message, subject are required)"""
    if request.method == 'POST':
        all_data = request.data
        try:
            serializer = MessagesSerializer(data=all_data)
            if serializer.is_valid():
                serializer.save()
                return Response(b'OK', status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
