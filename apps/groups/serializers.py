from rest_framework.serializers import ModelSerializer

from groups.models import Branch, Room, Course, Holiday, CourseGroup
from users.serializers import UserListModelSerializer, UserBranchListModelSerializer


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


class GroupModelSerializer(ModelSerializer):

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['teacher'] = [UserListModelSerializer(instance.teacher).data]
        data['room'] = [RoomListModelSerializer(instance.room).data]
        data['course'] = [CourseModelSerializer(instance.course).data]
        return data

    class Meta:
        model = CourseGroup
        fields = '__all__'


class RetrieveGroupModelSerializer(ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['teacher'] = [UserListModelSerializer(instance.teacher).data]
        data['room'] = [RoomListModelSerializer(instance.room).data]
        data['course'] = [CourseModelSerializer(instance.course).data]
        data['students'] = [UserListModelSerializer(obj).data for obj in instance.get_students]
        data['students_count'] = instance.students_count
        return data

    class Meta:
        model = CourseGroup
        fields = '__all__'


class HolidayListModelSerializer(ModelSerializer):
    class Meta:
        model = Holiday
        fields = 'name', 'holiday_date', 'affect_payment', 'branch', 'created_at'


class HolidayCreateModelSerializer(ModelSerializer):
    class Meta:
        model = Holiday
        fields = 'name', 'holiday_date', 'affect_payment'
