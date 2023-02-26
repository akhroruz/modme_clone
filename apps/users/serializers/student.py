from django.contrib.auth.hashers import make_password
from django.forms import model_to_dict
from rest_framework.fields import SerializerMethodField, CharField
from rest_framework.serializers import ModelSerializer

from users.models import Comment, User


class StudentListCommentModelSerializer(ModelSerializer):
    creater = SerializerMethodField()

    def get_creater(self, obj: Comment):  # noqa
        return model_to_dict(obj.creater, ('id', 'phone', 'first_name'))

    class Meta:
        model = Comment
        fields = ('id', 'text', 'creater')


class StudentListModelSerializer(ModelSerializer):
    branches = SerializerMethodField()
    groups = SerializerMethodField()

    def get_branches(self, obj: User):  # noqa
        return obj.branch.values('id', 'name')

    def get_groups(self, obj: User):  # noqa
        return obj.groups.all()

    class Meta:
        model = User
        fields = (
            'id', 'full_name', 'gender', 'birth_date', 'phone', 'photo', 'balance', 'deleted_at', 'data', 'is_archive',
            'branches', 'groups')
        read_only_fields = ('phone', 'full_name', 'id')

    def to_representation(self, instance: User):
        rep = super().to_representation(instance)
        rep['comment'] = StudentListCommentModelSerializer(instance.comment, many=True).data
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
