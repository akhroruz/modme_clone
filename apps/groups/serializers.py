from rest_framework.serializers import ModelSerializer

from apps.groups.models import Role, Branch, Room, Course, Holiday, Group
from apps.users.models import User


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


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'uuid', 'full_name', 'phone'


class GroupModelSerializer(ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['teacher'] = [UserModelSerializer(instance.teacher).data]
        data['room'] = [RoomListModelSerializer(instance.room).data]
        data['course'] = [CourseModelSerializer(instance.course).data]
        return data

    class Meta:
        model = Group
        fields = '__all__'


class RetrieveGroupModelSerializer(ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['teacher'] = [UserModelSerializer(instance.teacher).data]
        data['room'] = [RoomListModelSerializer(instance.room).data]
        data['course'] = [CourseModelSerializer(instance.course).data]
        data['students'] = [UserModelSerializer(obj).data for obj in instance.get_students]
        data['students_count'] = instance.students_count
        return data

    class Meta:
        model = Group
        fields = '__all__'


class HolidayListModelSerializer(ModelSerializer):
    class Meta:
        model = Holiday
        fields = 'name', 'holiday_date', 'affect_payment', 'branch', 'created_at'


class HolidayCreateModelSerializer(ModelSerializer):
    class Meta:
        model = Holiday
        fields = 'name', 'holiday_date', 'affect_payment'
