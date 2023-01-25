from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from apps.models import Role, Branch, Room, Course, Weekend, Group
from apps.serializers import RoleModelSerializer, BranchModelSerializer, RoomModelSerializer, CourseModelSerializer, \
    WeekendModelSerializer, GroupModelSerializer


class RoleModelViewSet(ModelViewSet):
    serializer_class = RoleModelSerializer
    queryset = Role.objects.all()


class BranchModelViewSet(ModelViewSet):
    serializer_class = BranchModelSerializer
    queryset = Branch.objects.all()


class RoomModelViewSet(ModelViewSet):
    serializer_class = RoomModelSerializer
    queryset = Room.objects.all()


class CourseModelViewSet(ModelViewSet):
    serializer_class = CourseModelSerializer
    queryset = Course.objects.all()


class WeekendModelViewSet(ModelViewSet):
    serializer_class = WeekendModelSerializer
    queryset = Weekend.objects.all()


class GroupModelViewSet(ModelViewSet):
    serializer_class = GroupModelSerializer
    queryset = Group.objects.all()
