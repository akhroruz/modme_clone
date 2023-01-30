from rest_framework.serializers import ModelSerializer

from apps.groups.models import Role, Branch, Room, Course, Weekend, Group


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


class WeekendModelSerializer(ModelSerializer):
    class Meta:
        model = Weekend
        fields = '__all__'


class GroupModelSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
