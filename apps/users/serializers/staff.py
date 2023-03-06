from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group as Role
from django.forms import model_to_dict
from rest_framework.fields import SerializerMethodField, ListField, CharField, ChoiceField
from rest_framework.serializers import ModelSerializer

from groups.models import Branch
from users.models import Comment, User


class StaffListCommentModelSerializer(ModelSerializer):
    author = SerializerMethodField()

    def get_author(self, obj: Comment):  # noqa
        return model_to_dict(obj.author, ('id', 'phone', 'first_name'))

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author')


class StaffListBranchModelSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = ('id', 'name')


class StaffListModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id', 'full_name', 'gender', 'birth_date', 'phone', 'photo', 'balance', 'deleted_at', 'data',
            'roles', 'number_of_groups', 'company_id')
        read_only_fields = ('phone', 'full_name', 'id')

    def to_representation(self, instance: User):
        rep = super().to_representation(instance)
        rep['comment'] = StaffListCommentModelSerializer(instance.comment, many=True).data
        rep['branches'] = StaffListBranchModelSerializer(instance.branch, many=True).data
        return rep


class StaffCreateModelSerializer(ModelSerializer):
    role = ListField(write_only=True)
    password = CharField(write_only=True, required=False)
    user_type = ChoiceField(choices=User.UserTypeChoice.choices)

    class Meta:
        model = User
        fields = (
            'branch', 'data', 'birth_date', 'gender', 'first_name', 'password', 'phone', 'photo', 'role',
            'user_type', 'group_set')

    def create(self, validated_data):
        validated_data['role'] = Role.objects.filter(name__in=validated_data.get('role')[0].split(','))
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)
