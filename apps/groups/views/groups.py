from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from apps.groups.models import Group
from apps.groups.serializers import GroupModelSerializer


class GroupModelViewSet(ModelViewSet):
    queryset = Group.objects.order_by('-created_at')
    serializer_class = GroupModelSerializer
    lookup_field = 'uuid'

    def list(self, request, *args, **kwargs):
        data = {
            'data': self.get_serializer(self.get_queryset(), many=True).data
        }
        return Response(data, status.HTTP_200_OK)

    # def retrieve(self, request, *args, **kwargs):

