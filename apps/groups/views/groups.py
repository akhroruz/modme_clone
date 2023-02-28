from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from groups.filters import CustomGroupDjangoFilterBackend, GroupFilter
from groups.models import Group
from groups.serializers import GroupListModelSerializer
from shared.utils.export_excel import export_data_excel

branch_id = openapi.Parameter(
    'branch',
    openapi.IN_QUERY,
    'Branch ID',
    True,
    type=openapi.TYPE_INTEGER
)


class GroupModelViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupListModelSerializer
    permission_classes = AllowAny,
    filter_backends = CustomGroupDjangoFilterBackend,
    filterset_class = GroupFilter

    def list(self, request, *args, **kwargs):
        params = self.request.query_params
        if not (params.get('page') and params.get('per_page')):
            self.pagination_class = None
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(manual_parameters=[branch_id])
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = GroupListModelSerializer(instance=instance)
        return Response(serializer.data)

    @action(['GET'], False, 'export', 'export')
    def export_users_xls(self, request):
        columns = ['ID', 'Name', 'Course', 'Teacher', 'Days', 'From', 'To', 'Room']
        rows = Group.objects.values_list(
            'id', 'name', 'course__name', 'teachers__first_name', 'days', 'start_date', 'end_date', 'room__name'
        )
        return export_data_excel(columns, rows)
