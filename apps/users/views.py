import pandas as pd
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from groups.filters import CustomCompanyDjangoFilterBackend
from shared.utils.export_excel import export_data_excel
from users.filters import UserFilter, CustomUserDjangoFilterBackend
from users.models import User, LeadIncrement, Lead, Blog
from users.serializers import LeadIncrementModelSerializer, \
    LeadModelSerializer, UpdateProfileSerializer, BlogModelSerializer, \
    StudentListModelSerializer, StaffListModelSerializer, StudentCreateModelSerializer, StaffCreateModelSerializer

from users.serializers.archive import ArchiveUserCreateModelSerializer
from users.serializers.lead import LeadImportSerializer
from users.serializers.user import UserDeleteModelSerializer


# https://api.modme.dev/v1/user?user_type=student&per_page=50&page=1&branch_id=189
class UserModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = StaffCreateModelSerializer
    parser_classes = MultiPartParser, FormParser
    filter_backends = DjangoFilterBackend, OrderingFilter
    filterset_class = UserFilter
    ordering = ('first_name', 'last_name')
    http_method_names = ('post', 'get', 'put', 'patch', 'delete')

    reason_id = openapi.Parameter('reason', openapi.IN_QUERY, 'Reason ID', True, type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[reason_id])
    def destroy(self, request, *args, **kwargs):
        reason = request.query_params.get('reason')
        user = self.get_queryset().filter(id=self.kwargs.get('pk'))
        serializer = ArchiveUserCreateModelSerializer(user, reason)
        serializer.save()  # TODO:
        return super().destroy(request, *args, **kwargs)

    # def perform_destroy(self, instance):
    #     serializer = ArchiveUserCreateModelSerializer(instance)
    #     serializer.save()
    #     super().perform_destroy(instance)

    def filter_queryset(self, queryset):
        if self.action in ('list', 'retrieve'):
            self.filter_backends = CustomUserDjangoFilterBackend, OrderingFilter
        return super().filter_queryset(queryset)

    def list(self, request, *args, **kwargs):
        params = self.request.query_params
        if not (params.get('page') and params.get('per_page')):
            self.pagination_class = None
        return super().list(request, *args, **kwargs)

    branch_id = openapi.Parameter('branch', openapi.IN_QUERY, 'Branch ID', True, type=openapi.TYPE_INTEGER)
    user_type = openapi.Parameter('user_type', openapi.IN_QUERY, 'User Type', True, type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[branch_id, user_type])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_serializer_class(self):
        user_type = self.request.POST.get('user_type')
        if self.action == 'create':
            if user_type == 'student':
                return StudentCreateModelSerializer
            return StaffCreateModelSerializer
        elif self.action in ('list', 'retrieve'):
            if user_type == 'student':
                return StudentListModelSerializer
            return StaffListModelSerializer
        return super().get_serializer_class()

    @action(('GET',), False, 'trashed', 'trashed')
    def get_trashed(self, request):
        queryset = User.objects.filter(deleted_at__isnull=True)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @action(('GET',), False, 'export', 'export')
    def export_users_xls(self, request):
        columns = ['ID', 'Name', 'Phone', 'Birthday', 'Comments', 'Balance']
        rows = User.objects.values_list('id', 'first_name', 'phone', 'birth_date', 'comment', 'balance')
        return export_data_excel(columns, rows)

    # @action(('DELETE',), True)
    # def delete_user(self, request, id, reason_id):


# class UserDocumentView(DocumentViewSet):
#     document = UserDocument
#     serializer_class = UserListDocumentSerializer
#     permission_classes = AllowAny,
#     filter_backends = SearchFilterBackend,
#     search_fields = 'first_name', 'last_name', 'phone'


# https://fastapi.modme.dev/api/v1/leads/?branch_id=189&company_id=131
class LeadIncrementModelViewSet(ModelViewSet):
    serializer_class = LeadIncrementModelSerializer
    queryset = LeadIncrement.objects.all()
    permission_classes = (AllowAny,)


class LeadModelViewSet(ModelViewSet):
    serializer_class = LeadModelSerializer
    queryset = Lead.objects.all()
    permission_classes = (AllowAny,)

    def list(self, request, *args, **kwargs):
        qs = self.get_queryset()
        data = {
            'count': qs.count(),
            'data': self.get_serializer(qs, many=True).data
        }
        return Response(data)

    @action(['GET'], False, 'export', 'export')
    def export_leads_xls(self, request):
        columns = ['Id', 'Full_Name', 'Comment', 'Phone', 'Status', 'Source']
        rows = Lead.objects.values_list(
            'id', 'full_name', 'comment', 'phone', 'status', 'lead_increment__name'
        )
        return export_data_excel(columns, rows)

    @swagger_auto_schema(operation_description='Upload file')
    @action(['POST'], False, parser_classes=(MultiPartParser,), serializer_class=LeadImportSerializer)
    def import_data(self, request):
        file = request.FILES['file']
        df = pd.read_excel(file)

        data = []
        for index, row in df.iterrows():
            source = LeadIncrement.objects.create(name=row['Source'])
            data.append(Lead(
                full_name=row['Full_Name'],
                comment=row['Comment'],
                phone=row['Phone'],
                status=row['Status'],
                lead_increment=source,
            ))
        Lead.objects.bulk_create(data)
        return Response({'message': 'Data imported successfully'})


class UpdateProfileView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateProfileSerializer


# https://api.modme.dev/v1/blog/?company_id=131
class BlogModelViewSet(ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogModelSerializer
    filter_backends = CustomCompanyDjangoFilterBackend,
    filterset_fields = 'company',  # noqa

    company = openapi.Parameter('company', openapi.IN_QUERY, 'Company ID', True, type=openapi.TYPE_INTEGER)

    @swagger_auto_schema(manual_parameters=[company])
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        qs = super().get_queryset()
        qs.update(view_count=F('view_count') + 1)
        return qs
