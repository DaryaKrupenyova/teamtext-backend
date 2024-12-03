import logging.config

import jwt
from django.conf.global_settings import SECRET_KEY
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from base.models import Document
from base.tt_serializers.document_serializer import DocumentSerializer

logger = logging.getLogger(__name__)


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return Document.objects.filter(users=self.request.user)


class AddCollaboratorAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = self.request.user
        token = request.query_params.get('token', None)
        if token is not None:
            try:
                decoded_jwt = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
                if decoded_jwt['is_editor']:
                    role = 'editor'
                else:
                    role = 'viewer'
                document = Document.objects.get(id=decoded_jwt['file_id'])
                document.users.add(user, through_defaults={"role": role})
                return Response(data="Success!", status=status.HTTP_200_OK)
            except jwt.ExpiredSignatureError:
                return Response(data="Token expired.", status=status.HTTP_403_FORBIDDEN)
            except jwt.DecodeError:
                return Response(data="Bad token.", status=status.HTTP_403_FORBIDDEN)
            except:
                return Response(data="Server fault.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data="Token missing.", status=status.HTTP_400_BAD_REQUEST)
