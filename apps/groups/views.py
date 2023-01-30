from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListCreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet

from apps.groups.models import Role, Branch, Room, Course, Weekend, Group
from apps.groups.serializers import RoleModelSerializer, BranchModelSerializer, \
    CourseModelSerializer, \
    WeekendModelSerializer, GroupModelSerializer
from groups.serializers import RoomListModelSerializer, RoomCreateModelSerializer


class RoleModelViewSet(ModelViewSet):
    serializer_class = RoleModelSerializer
    queryset = Role.objects.all()


class BranchModelViewSet(ModelViewSet):
    serializer_class = BranchModelSerializer
    queryset = Branch.objects.all()
    parser_classes = (MultiPartParser,)


class CourseModelViewSet(ModelViewSet):
    serializer_class = CourseModelSerializer
    queryset = Course.objects.all()


class WeekendModelViewSet(ModelViewSet):
    serializer_class = WeekendModelSerializer
    queryset = Weekend.objects.all()


class GroupModelViewSet(ModelViewSet):
    serializer_class = GroupModelSerializer
    queryset = Group.objects.all()


class RoomModelViewSet(ModelViewSet):
    serializer_class = RoomCreateModelSerializer
    queryset = Room.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('branch',)

    def get_serializer_class(self):
        if self.action == 'list':
            return RoomListModelSerializer
        return super().get_serializer_class()
