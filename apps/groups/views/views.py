from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet

from groups.filters import CustomCompanyDjangoFilterBackend, CustomBranchDjangoFilterBackend
from groups.models import Branch, Room, Course, Company, Holiday
from groups.serializers import BranchModelSerializer, RoomListModelSerializer, HomeModelSerializer, \
    CompanyModelSerializer, BranchListModelSerializer, RoomCreateModelSerializer, CourseCreateModelSerializer, \
    CourseListModelSerializer, HolidayCreateModelSerializer, HolidayListModelSerializer


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
    serializer_class = RoomCreateModelSerializer
    queryset = Room.objects.all()
    # permission_classes = IsAuthenticated, DjangoObjectPermissions, IsAdministrator
    filter_backends = DjangoFilterBackend,
    filterset_fields = 'branch',

    branch_id = openapi.Parameter('branch', openapi.IN_QUERY, 'Branch ID', True, type=openapi.TYPE_INTEGER)

    def get_object(self):
        return super().get_object()

    @swagger_auto_schema(manual_parameters=[branch_id])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            self.filter_backends = [CustomBranchDjangoFilterBackend]
            return RoomListModelSerializer
        return super().get_serializer_class()


# https://api.modme.dev/v1/company/subdomain/demo
class HomeListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = HomeModelSerializer


class CompanyModelViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanyModelSerializer
    parser_classes = (MultiPartParser,)
    # permission_classes = IsAuthenticated, DjangoObjectPermissions, IsAdministrator


# https://api.modme.dev/v1/course?company_id=131
class CourseModelViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseCreateModelSerializer
    filter_backends = DjangoFilterBackend,
    filterset_fields = 'company',
    # permission_classes = IsAuthenticated, DjangoObjectPermissions, IsAdministrator
    company_id = openapi.Parameter('company', openapi.IN_QUERY, 'Company ID', True, type=openapi.TYPE_INTEGER)

    def get_object(self):
        return super().get_object()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            self.filter_backends = [CustomBranchDjangoFilterBackend]
            return CourseListModelSerializer
        return super().get_serializer_class()

    @swagger_auto_schema(manual_parameters=[company_id])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


# https://api.modme.dev/v1/holiday?branch_id=189
class HolidayModelViewSet(ModelViewSet):
    queryset = Holiday.objects.all()
    serializer_class = HolidayCreateModelSerializer
    filterset_fields = 'branch',
    filter_backends = DjangoFilterBackend,

    branch_id = openapi.Parameter('branch', openapi.IN_QUERY, 'Branch ID', True, type=openapi.TYPE_INTEGER)

    def get_object(self):
        return super().get_object()

    @swagger_auto_schema(manual_parameters=[branch_id])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            self.filter_backends = [CustomBranchDjangoFilterBackend]
            return HolidayListModelSerializer
        return super().get_serializer_class()

# https://api.modme.dev/v1/archiveReasons?company_id=131
# class ArchiveReasonsModelViewSet(ModelViewSet):
#     queryset = Archive.objects.all()
#     serializer_class = ArchiveListModelSerializer
#     filter_backends = CustomCompanyDjangoFilterBackend,
#     filterset_fields = 'company',
#     # permission_classes = [IsAdministrator, CustomDjangoObjectPermissions]
#     # http_method_names = ['get', 'post', 'put', 'patch']
#
#     company_id = openapi.Parameter('company', openapi.IN_QUERY, 'Company ID', True, type=openapi.TYPE_INTEGER)
#
#     def get_serializer_class(self):
#         if self.action == 'list':
#             return ArchiveListModelSerializer
#         return super().get_serializer_class()
#
#     @swagger_auto_schema(manual_parameters=[company_id])
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = ArchiveListModelSerializer(instance=instance)
#         return Response(serializer.data)

# https://api.modme.dev/v1/company/subdomain/demo
# https://api.modme.dev/v1/auth/me
