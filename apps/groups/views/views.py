from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions
from rest_framework.viewsets import ModelViewSet

from groups.filters import CustomCompanyDjangoFilterBackend
from groups.models import Branch, Room, Course, Company
from groups.serializers import BranchModelSerializer, RoomListModelSerializer, RoomCreateModelSerializer, \
    HomeModelSerializer, CompanyModelSerializer
from shared.permissions import IsAdministrator


class BranchModelViewSet(ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchModelSerializer
    filter_backends = CustomCompanyDjangoFilterBackend,
    filterset_fields = 'company',
    parser_classes = (MultiPartParser,)


class RoomModelViewSet(ModelViewSet):
    serializer_class = RoomCreateModelSerializer
    queryset = Room.objects.all()
    permission_classes = IsAuthenticated, DjangoObjectPermissions, IsAdministrator

    def get_serializer_class(self):
        if self.action == 'list':
            return RoomListModelSerializer
        return super().get_serializer_class()


class HomeListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = HomeModelSerializer


class CompanyModelViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanyModelSerializer
    permission_classes = IsAuthenticated, DjangoObjectPermissions, IsAdministrator