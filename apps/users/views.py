from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.openapi import Schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, AllowAny, DjangoObjectPermissions
from rest_framework.viewsets import ModelViewSet

from shared.permissions import IsAdministrator
from users.models import User, LidIncrement, Lid
from users.serializers import UserListModelSerializer, ChangePasswordSerializer, \
    UserCreateModelSerializer, LidIncrementModelSerializer, LidModelSerializer


class UserModelViewSet(ModelViewSet):
    serializer_class = UserListModelSerializer
    queryset = User.objects.all()
    # permission_classes = AllowAny,
    parser_classes = (MultiPartParser,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name', 'id', 'phone', 'role__name']
    ordering = ['first_name', 'last_name']

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateModelSerializer
        return super().get_serializer_class()

    # role = openapi.Parameter('role', in_=openapi.IN_FORM, type=openapi.TYPE_ARRAY,
    #                          items=openapi.Items(type=openapi.TYPE_STRING))

    # @swagger_auto_schema(
    #     tags=['botirjon'],
    #     request_body=UserCreateModelSerializer,
    # )

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class LidIncrementModelViewSet(ModelViewSet):
    serializer_class = LidIncrementModelSerializer
    queryset = LidIncrement.objects.all()


class LidModelViewSet(ModelViewSet):
    serializer_class = LidModelSerializer
    queryset = Lid.objects.all()
    permission_classes = (DjangoObjectPermissions, IsAdministrator)


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
