from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.permissions import DjangoObjectPermissions, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from groups.models import CourseGroup
from groups.serializers import GroupListModelSerializer


class GroupModelViewSet(ModelViewSet):
    queryset = CourseGroup.objects.order_by('-created_at')
    serializer_class = GroupListModelSerializer
    permission_classes = DjangoObjectPermissions, IsAuthenticated
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('branch', 'status', 'teachers__first_name', 'course', 'days', 'start_date', 'end_date')

    def list(self, request, *args, **kwargs):
        data = {
            'data': self.get_serializer(self.get_queryset(), many=True).data
        }
        return Response(data, status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = GroupListModelSerializer(instance=instance)
        return Response(serializer.data)
