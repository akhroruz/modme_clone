from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from users.models import User, LidIncrement, Lid
from users.serializers import UserListModelSerializer, ChangePasswordSerializer, \
    UserCreateModelSerializer, LidIncrementModelSerializer, LidModelSerializer


class UserModelViewSet(ModelViewSet):
    serializer_class = UserListModelSerializer
    queryset = User.objects.all()
    parser_classes = (MultiPartParser,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name', 'id', 'phone', 'role__name']
    ordering = ['first_name', 'last_name']

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateModelSerializer
        return super().get_serializer_class()


class LidIncrementModelViewSet(ModelViewSet):
    serializer_class = LidIncrementModelSerializer
    queryset = LidIncrement.objects.all()


class LidModelViewSet(ModelViewSet):
    serializer_class = LidModelSerializer
    queryset = Lid.objects.all()


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer
