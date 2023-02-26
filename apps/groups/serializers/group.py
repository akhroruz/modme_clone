from rest_framework.serializers import ModelSerializer

from groups.models import Course, Group, Room
from users.models import User


class GroupRoomListModelSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class GroupCourseListModelSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'name', 'price')


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
        data['teacher'] = GroupTeacherListModelSerializer(instance.teacher).data
        data['room'] = GroupRoomListModelSerializer(instance.room).data
        data['course'] = GroupCourseListModelSerializer(instance.course).data
        return data
