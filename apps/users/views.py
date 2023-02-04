from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions, AllowAny
from rest_framework.viewsets import ModelViewSet

from shared.permissions import IsAdministrator
from users.models import User, LeadIncrement, Lead, Archive
from users.serializers import ArchiveListModelSerializer, UserListModelSerializer, UserCreateModelSerializer, \
    LidIncrementModelSerializer, LidModelSerializer, ChangePasswordSerializer, UpdateProfileSerializer


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

    @action(methods=['GET', 'POST'], detail=False, url_path='trashed', url_name='trashed')
    def get_trashed(self, request):
        if self.request.method == 'GET':
            serializer = ArchiveListModelSerializer(Archive.objects.all(), many=True)
            return Response(serializer.data)
        if self.request.method == 'POST':
            gender = request.data.get('gender')
            birth_date = request.data.get('birth_date')
            phone = request.data.get('phone')
            photo = request.data.get('photo')
            balance = request.data.get('balance')
            deleted_at = request.data.get('deleted_at')
            datas = request.data.get('datas')
            user = User.objects.create(gender=gender, birth_date=birth_date, phone=phone, photo=photo, balance=balance,
                                       deleted_at=deleted_at, datas=datas, is_archive=True)


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


class ArchiveReasonsModelViewSet(ModelViewSet):
    queryset = Archive.objects.all()
    serializer_class = ArchiveListModelSerializer


class UpdateProfileView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateProfileSerializer
