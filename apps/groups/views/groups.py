from django_filters.rest_framework import DjangoFilterBackend  # OrderingFilter
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from rest_framework.viewsets import ModelViewSet

from groups.filters import CustomGroupDjangoFilterBackend, GroupFilter
from groups.models import Group
from groups.serializers import GroupListModelSerializer
from shared.utils.export_excel import export_data_excel
from users.models import User
from users.serializers import StudentListModelSerializer


# https://api.modme.dev/v1/group?branch_id=189&per_page=200&page=1
class GroupModelViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupListModelSerializer
    filter_backends = DjangoFilterBackend,
    filterset_class = GroupFilter

    def filter_queryset(self, queryset):
        if self.action in ('list', 'retrieve'):
            self.filter_backends = CustomGroupDjangoFilterBackend,
        return super().filter_queryset(queryset)

    def list(self, request, *args, **kwargs):
        params = self.request.query_params
        if not (params.get('page') and params.get('per_page')):
            self.pagination_class = None
        return super().list(request, *args, **kwargs)

    branch_id = openapi.Parameter('branch', openapi.IN_QUERY, 'Branch ID', True, type=openapi.TYPE_INTEGER)

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

    # https://api.modme.dev/v1/group/13119/students/31739
    @action(['POST'], True, 'students/(?P<student_id>\d+)', 'students',  # noqa
            serializer_class=None)
    def add_students(self, request, pk=None, student_id=None):
        """
        API to add a **student** to a group.
        """
        student = User.objects.get(id=student_id)
        if student.role.filter(user__user_type='student').exists():
            group = Group.objects.get(id=pk)
            group.students.add(student)
            group.save()
            return Response(StudentListModelSerializer(student).data)
        return Response({'status': 'Error'}, status=HTTP_400_BAD_REQUEST)
