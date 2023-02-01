from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from groups.models import CourseGroup
from groups.serializers import GroupModelSerializer, RetrieveGroupModelSerializer


class GroupModelViewSet(ModelViewSet):
    queryset = CourseGroup.objects.order_by('-created_at')
    serializer_class = GroupModelSerializer

    def list(self, request, *args, **kwargs):
        data = {
            'data': self.get_serializer(self.get_queryset(), many=True).data
        }
        return Response(data, status.HTTP_200_OK)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = RetrieveGroupModelSerializer(instance=instance)
        return Response(serializer.data)