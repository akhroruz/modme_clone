from django.forms import model_to_dict
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from users.models import Comment, User


class StaffListCommentModelSerializer(ModelSerializer):
    creater = SerializerMethodField()

    def get_creater(self, obj: Comment):  # noqa
        return model_to_dict(obj.creater, ('id', 'phone', 'first_name'))

    class Meta:
        model = Comment
        fields = ('id', 'text', 'creater')


class StaffListModelSerializer(ModelSerializer):
    roles = SerializerMethodField()
    branches = SerializerMethodField()
    company_id = SerializerMethodField()

    def get_roles(self, obj: User):  # noqa
        return obj.role.values('id', 'name')

    def get_branches(self, obj: User):  # noqa
        return obj.branch.values('id', 'name')

    def get_company_id(self, obj: User):
        return obj.branch.first().company_id

    class Meta:
        model = User
        fields = (
            'id', 'full_name', 'gender', 'birth_date', 'phone', 'photo', 'balance', 'company_id', 'deleted_at', 'data',
            'roles', 'is_archive', 'branches')
        read_only_fields = ('phone', 'full_name', 'id')

    def to_representation(self, instance: User):
        rep = super().to_representation(instance)
        rep['comment'] = StaffListCommentModelSerializer(instance.comment, many=True).data
        return rep
