from rest_framework.serializers import ModelSerializer

from groups.models import Branch, Room, Course, Holiday, Group, Company
from users.models import User
from users.serializers import UserBranchListModelSerializer


class CompanyModelSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class BranchModelSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'


class RoomListModelSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name')


class RoomCreateModelSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class HomeModelSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def to_representation(self, instance: Course):
        rep = super().to_representation(instance)
        rep['branches'] = UserBranchListModelSerializer(instance.branch, many=True).data
        return rep


class HolidayModelSerializer(ModelSerializer):
    class Meta:
        model = Holiday
        fields = '__all__'


class CourseListModelSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ('name', 'price')


class GroupTeacherListModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'phone')


class GroupListModelSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

    def to_representation(self, instance: Group):
        data = super().to_representation(instance)
        data['students_count'] = instance.students_count
        data['teachers'] = GroupTeacherListModelSerializer(instance.teachers, many=True).data
        data['room'] = RoomListModelSerializer(instance.room, many=True).data
        data['course'] = CourseListModelSerializer(instance.course).data
        return data


class HolidayListModelSerializer(ModelSerializer):
    class Meta:
        model = Holiday
        fields = 'name', 'holiday_date', 'affect_payment', 'branch', 'created_at'


class HolidayCreateModelSerializer(ModelSerializer):
    class Meta:
        model = Holiday
        fields = 'name', 'holiday_date', 'affect_payment'


class GroupModelSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
