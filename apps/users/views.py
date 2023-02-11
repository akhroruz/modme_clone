from django.db.models import F
from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from shared.permissions import IsAdministrator
from shared.utils.export_excel import export_data_excel
from users.documents import UserDocument
from users.filters import UserFilter, CustomDjangoFilterBackend
from users.models import User, LeadIncrement, Lead, Archive, Blog
from users.serializers import ArchiveListModelSerializer, UserListModelSerializer, UserCreateModelSerializer, \
    LeadIncrementModelSerializer, LeadModelSerializer, UpdateProfileSerializer, \
    BlogModelSerializer, ArchiveCreateModelSerializer, UserListDocumentSerializer


class UserModelViewSet(ModelViewSet):
    serializer_class = UserListModelSerializer
    queryset = User.objects.all()
    permission_classes = AllowAny,
    parser_classes = MultiPartParser,
    filter_backends = CustomDjangoFilterBackend,
    filterset_class = UserFilter
    ordering = ['first_name', 'last_name']

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateModelSerializer
        return super().get_serializer_class()

    @action(methods=['GET', 'POST'], detail=False, url_path='trashed', url_name='trashed')
    def get_trashed(self, request):
        if self.request.method == 'GET':
            serializer = ArchiveListModelSerializer(Archive.objects.all(), many=True)
            return Response(serializer.data)
        if self.request.method == 'POST':
            serializer = ArchiveCreateModelSerializer(request.data)
            serializer.save()
            return Response(serializer.data)

    # @action(['GET'], False,url_path='branch', filter_backends=(CustomDjangoFilterBackend,), filterset_class=UserFilter)
    # def user(self, request):
    #     filtered_query_set = self.filter_queryset(self.get_queryset())
    #     branch_id = [1]
    #     qs = self.get_queryset()
    #     serializer = UserListModelSerializer(qs.filter(branch__in=branch_id), many=True).data
    #     return Response(serializer)

    @action(['GET'], False, 'export', 'export')
    def export_users_xls(self, request):

        columns = ['ID', 'Name', 'Phone', 'Birthday', 'Comments', 'Balance']
        rows = User.objects.values_list('id', 'first_name', 'phone', 'birth_date', 'comment', 'balance')
        return export_data_excel(columns, rows)


'''
https://api.modme.dev/v1/user?user_type=student&per_page=50&page=1&course_id=969,968,966&statuses=with_signed_offer,1&branch_id=189
https://api.modme.dev/v1/user/branch/<branch:id>

'''


class UserDocumentView(DocumentViewSet):
    document = UserDocument
    serializer_class = UserListDocumentSerializer
    permission_classes = AllowAny,
    filter_backends = SearchFilterBackend,
    search_fields = 'first_name', 'last_name', 'phone'


class LeadIncrementModelViewSet(ModelViewSet):
    serializer_class = LeadIncrementModelSerializer
    queryset = LeadIncrement.objects.all()


class LeadModelViewSet(ModelViewSet):
    serializer_class = LeadModelSerializer
    queryset = Lead.objects.all()
    permission_classes = (DjangoObjectPermissions, IsAdministrator)


class ArchiveReasonsModelViewSet(ModelViewSet):
    queryset = Archive.objects.all()
    serializer_class = ArchiveListModelSerializer


class UpdateProfileView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateProfileSerializer


class BlogModelViewSet(ModelViewSet):
    queryset = Blog.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = BlogModelSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs.update(view_count=F('view_count') + 1)
        return qs
