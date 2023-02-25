from django.db.models import F
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
from users.models import User, LeadIncrement, Lead, Archive, Blog
from users.serializers import ArchiveListModelSerializer, UserListModelSerializer, UserCreateModelSerializer, \
    LeadIncrementModelSerializer, LeadModelSerializer, UpdateProfileSerializer, BlogModelSerializer, \
    ArchiveCreateModelSerializer


class UserModelViewSet(ModelViewSet):
    serializer_class = UserListModelSerializer
    queryset = User.objects.all()
    permission_classes = AllowAny,
    parser_classes = MultiPartParser, FormParser
    filter_backends = CustomUserDjangoFilterBackend, OrderingFilter
    filterset_class = UserFilter
    ordering = ['first_name', 'last_name']

    def list(self, request, *args, **kwargs):
        if not self.request.query_params.get('per_page'):
            self.pagination_class = None
        return super().list(request, *args, **kwargs)

    # def paginate_queryset(self, queryset):
    #     # if self.request.query_params.get('per')
    #     if per_page := self.request.query_params.get('per_page'):
    #         return super().paginate_queryset(queryset)
    #     return queryset

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateModelSerializer
        return super().get_serializer_class()

    @action(['GET', 'POST'], False, 'trashed', 'trashed')
    def get_trashed(self, request):
        if self.request.method == 'GET':
            serializer = ArchiveListModelSerializer(Archive.objects.all(), many=True)
        else:
            serializer = ArchiveCreateModelSerializer(request.data)
            serializer.save()
        return Response(serializer.data)

    @action(['GET'], False, 'export', 'export')
    def export_users_xls(self, request):
        columns = ['ID', 'Name', 'Phone', 'Birthday', 'Comments', 'Balance']
        rows = User.objects.values_list('id', 'first_name', 'phone', 'birth_date', 'comment', 'balance')
        return export_data_excel(columns, rows)


# class UserDocumentView(DocumentViewSet):
#     document = UserDocument
#     serializer_class = UserListDocumentSerializer
#     permission_classes = AllowAny,
#     filter_backends = SearchFilterBackend,
#     search_fields = 'first_name', 'last_name', 'phone'


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


class ArchiveReasonsModelViewSet(ModelViewSet):
    queryset = Archive.objects.all()
    serializer_class = ArchiveListModelSerializer
    # permission_classes = [IsAdministrator, CustomDjangoObjectPermissions]
    # http_method_names = ['get', 'post', 'put', 'patch']


class UpdateProfileView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateProfileSerializer


class BlogModelViewSet(ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogModelSerializer
    filter_backends = CustomCompanyDjangoFilterBackend,
    filterset_fields = 'company',  # noqa

    def get_queryset(self):
        qs = super().get_queryset()
        qs.update(view_count=F('view_count') + 1)
        return qs
