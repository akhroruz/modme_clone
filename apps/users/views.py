from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions, AllowAny
from rest_framework.viewsets import ModelViewSet

from shared.permissions import IsAdministrator
from users.models import User, LeadIncrement, Lead
from users.serializers import UserListModelSerializer, UserCreateModelSerializer, LidIncrementModelSerializer, \
    LidModelSerializer, ChangePasswordSerializer, UpdateProfileSerializer


class UserModelViewSet(ModelViewSet):
    serializer_class = UserListModelSerializer
    queryset = User.objects.all()
    permission_classes = DjangoObjectPermissions,
    parser_classes = (MultiPartParser,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['first_name', 'last_name', 'id', 'phone', 'role__name']
    ordering = ['first_name', 'last_name']

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateModelSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class LeadIncrementModelViewSet(ModelViewSet):
    serializer_class = LidIncrementModelSerializer
    queryset = LeadIncrement.objects.all()


class LeadModelViewSet(ModelViewSet):
    serializer_class = LidModelSerializer
    queryset = Lead.objects.all()
    permission_classes = (DjangoObjectPermissions, IsAdministrator)


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class UpdateProfileView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateProfileSerializer
