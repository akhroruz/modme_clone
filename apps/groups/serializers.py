from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from apps.groups.models import Role, Branch, Room, Course, Holiday, Group
from apps.users.models import User
from apps.groups.models import Role, Branch, Room, Course, Holiday, Group


class RoleModelSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class BranchModelSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class RoomListModelSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ('uuid', 'name')


class RoomCreateModelSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class CourseModelSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class HolidayModelSerializer(ModelSerializer):
    class Meta:
        model = Holiday
        fields = '__all__'


class GroupModelSerializer(ModelSerializer):
    teacher = SerializerMethodField()

    class Meta:
        model = Group
        fields = '__all__'


class HolidayListModelSerializer(ModelSerializer):
    class Meta:
        model = Holiday
        fields = ('name', 'holiday_date', 'affect_payment', 'branch', 'created_at')


class HolidayCreateModelSerializer(ModelSerializer):
    class Meta:
        model = Holiday
        fields = ('name', 'holiday_date', 'affect_payment')
