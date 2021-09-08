from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_417_EXPECTATION_FAILED
)

from .serializers import ContactMessageSerializer


__all__ = ['ContactMessageView']


class ContactMessageView(APIView):
    permission_classes = (AllowAny,)
    
    # def get_serializer_context(self):
    #     return {
    #         'request': self.request,
    #     }

    def post(self, request, format=None):

        serializer = ContactMessageSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            message = serializer.save()
            message.send(do_save=True)
            return Response(
                {
                    'status': message.status,
                    'status_str': message.get_status_display()
                },
                status=HTTP_201_CREATED
            )