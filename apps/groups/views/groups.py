from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from groups.filters import CustomGroupDjangoFilterBackend, GroupFilter
from groups.models import CourseGroup
from groups.serializers import GroupListModelSerializer
from shared.utils.export_excel import export_data_excel


class GroupModelViewSet(ModelViewSet):
    queryset = CourseGroup.objects.order_by('-created_at')
    serializer_class = GroupListModelSerializer
    permission_classes = AllowAny
    filter_backends = (CustomGroupDjangoFilterBackend,)
    filterset_class = GroupFilter

    def list(self, request, *args, **kwargs):
        data = {
            'data': self.get_serializer(self.get_queryset(), many=True).data
        }
        return Response(data, status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = GroupListModelSerializer(instance=instance)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='export', url_name='export')
    def export_users_xls(self, request):
        columns = ['ID', 'Name', 'Course', 'Teacher', 'Days', 'From', 'To', 'Room']
        rows = CourseGroup.objects.values_list('id', 'name', 'course__name', 'teachers__first_name', 'days',
                                               'start_date', 'end_date', 'room__name')
        return export_data_excel(columns, rows)
