from django.contrib.auth.hashers import make_password
from django.forms import model_to_dict
from rest_framework.fields import SerializerMethodField, CharField
from rest_framework.serializers import ModelSerializer

from groups.models import Group, Room
from users.models import Comment, User


class StudentListCommentModelSerializer(ModelSerializer):
    creater = SerializerMethodField()  # noqa

    def get_creater(self, obj: Comment):  # noqa
        return model_to_dict(obj.creater, ('id', 'phone', 'first_name'))

    class Meta:
        model = Comment
        fields = ('id', 'text', 'creater')  # noqa


class StudentRoomListModelSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name')


class StudentGroupListModelSerializer(ModelSerializer):
    course = SerializerMethodField()
    teacher = SerializerMethodField()

    def get_course(self, obj: Group):  # noqa
        return model_to_dict(obj.course, (
            'id', 'name', 'description', 'lesson_duration', 'course_duration', 'price'
        ))

    def get_teacher(self, obj: Group):  # noqa
        return model_to_dict(obj.teacher, ('id', 'first_name', 'phone'))

    class Meta:
        model = Group
        fields = ('id', 'name', 'days', 'status', 'course', 'teacher')

    def to_representation(self, instance: Group):
        rep = super().to_representation(instance)
        rep['rooms'] = StudentRoomListModelSerializer(instance.room).data
        return rep


class StudentListModelSerializer(ModelSerializer):
    branches = SerializerMethodField()

    def get_branches(self, obj: User):  # noqa
        return obj.branch.values('id', 'name')

    class Meta:
        model = User
        fields = (
            'id', 'full_name', 'gender', 'birth_date', 'phone', 'photo', 'balance', 'deleted_at', 'data', 'is_archive',
            'branches')
        read_only_fields = ('phone', 'full_name', 'id')

    def to_representation(self, instance: User):
        rep = super().to_representation(instance)
        rep['comment'] = StudentListCommentModelSerializer(instance.comment, many=True).data
        rep['groups'] = StudentGroupListModelSerializer(instance.groups, many=True).data
        return rep


# TODO: Teacher create action'da user_type qanday aniqlash mumkin.
class StudentCreateModelSerializer(ModelSerializer):
    password = CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = (
            'branch', 'comment', 'data', 'birth_date', 'gender', 'groups', 'first_name', 'password', 'phone')

    def create(self, validated_data):
        if validated_data['password']:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def to_internal_value(self, data):
        data['user_type'] = 'student'
        return super().to_internal_value(data)
