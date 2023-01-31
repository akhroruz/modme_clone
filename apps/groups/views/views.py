from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet

from apps.groups.models import Branch, Room, Course, Holiday
from apps.groups.serializers import BranchModelSerializer, CourseModelSerializer, \
    HolidayModelSerializer, RoomListModelSerializer, RoomCreateModelSerializer



class BranchModelViewSet(ModelViewSet):
    serializer_class = BranchModelSerializer
    queryset = Branch.objects.all()
    parser_classes = (MultiPartParser,)


class CourseModelViewSet(ModelViewSet):
    serializer_class = CourseModelSerializer
    queryset = Course.objects.all()


class WeekendModelViewSet(ModelViewSet):
    serializer_class = HolidayModelSerializer
    queryset = Holiday.objects.all()


class RoomModelViewSet(ModelViewSet):
    serializer_class = RoomCreateModelSerializer
    queryset = Room.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return RoomListModelSerializer
        return super().get_serializer_class()
