from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions
from rest_framework.viewsets import ModelViewSet

from groups.filters import CustomCompanyDjangoFilterBackend, CustomBranchDjangoFilterBackend
from groups.models import Branch, Room, Course, Company, Holiday
from groups.serializers import BranchModelSerializer, RoomListModelSerializer, HomeModelSerializer, \
    CompanyModelSerializer, BranchListModelSerializer, HolidayListModelSerializer
from groups.serializers.serializers import CourseModelSerializer
from shared.permissions import IsAdministrator
from users.models import Archive
from users.serializers import ArchiveListModelSerializer


# https://api.modme.dev/v1/branch?company_id=131
class BranchModelViewSet(ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchModelSerializer
    filter_backends = CustomCompanyDjangoFilterBackend,
    filterset_fields = 'company',
    parser_classes = (MultiPartParser,)

    def get_serializer_class(self):
        if self.action == 'list':
            return BranchListModelSerializer
        return super().get_serializer_class()


# https://api.modme.dev/v1/room?branch_id=189
class RoomModelViewSet(ModelViewSet):
    serializer_class = RoomListModelSerializer
    queryset = Room.objects.all()
    # permission_classes = IsAuthenticated, DjangoObjectPermissions, IsAdministrator
    filter_backends = CustomBranchDjangoFilterBackend,
    filterset_fields = 'branch',

    def get_serializer_class(self):
        if self.action == 'list':
            return RoomListModelSerializer
        return super().get_serializer_class()


# https://api.modme.dev/v1/company/subdomain/demo
class HomeListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = HomeModelSerializer


class CompanyModelViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanyModelSerializer
    permission_classes = IsAuthenticated, DjangoObjectPermissions, IsAdministrator


# https://api.modme.dev/v1/course?company_id=131
class CourseModelViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseModelSerializer
    # permission_classes = IsAuthenticated, DjangoObjectPermissions, IsAdministrator


# https://api.modme.dev/v1/holiday?branch_id=189
class HolidayModelViewSet(ModelViewSet):
    queryset = Holiday.objects.all()
    serializer_class = HolidayListModelSerializer
    filter_backends = CustomBranchDjangoFilterBackend,
    filterset_fields = 'branch',


# https://api.modme.dev/v1/archiveReasons?company_id=131
class ArchiveReasonsModelViewSet(ModelViewSet):
    queryset = Archive.objects.all()
    serializer_class = ArchiveListModelSerializer
    filter_backends = CustomCompanyDjangoFilterBackend,
    filterset_fields = 'company',
    # permission_classes = [IsAdministrator, CustomDjangoObjectPermissions]
    # http_method_names = ['get', 'post', 'put', 'patch']

# TODO: Teacher tuhunarsiz
# https://api.modme.dev/v1/company/subdomain/demo
