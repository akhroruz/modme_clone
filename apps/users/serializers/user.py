from django.contrib.auth.hashers import make_password
from rest_framework.exceptions import ValidationError
from rest_framework.fields import ListField, CharField, IntegerField
from rest_framework.serializers import ModelSerializer

from groups.models import Group
from users.models import User, Blog


class UserCreateRoleModelSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserCreateModelSerializer(ModelSerializer):
    role = ListField(write_only=True)
    password = CharField(write_only=True, required=False)
    user_type = CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'branch',
            'phone', 'user_type', 'first_name', 'gender',
            'birth_date', 'photo', 'data', 'role', 'password'
        )

    def create(self, validated_data):
        validated_data['role'] = Group.objects.filter(name__in=validated_data['role'][0].split(','))
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UpdateProfileSerializer(ModelSerializer):
    phone = IntegerField(required=True)

    class Meta:
        model = User
        fields = 'first_name', 'phone', 'role', 'birth_date', 'gender', 'photo', 'password'

    def validate_phone(self, phone):  # noqa
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(phone=phone).exists():
            raise ValidationError({'phone': "This phone is already in use."})
        return phone


class BlogModelSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = ('title', 'text', 'public', 'visible_all', 'view_count', 'company')
        extra_kwargs = {
            'created_by': {'required': False},
            'updated_by': {'required': False},
            'view_count': {'required': False},
            'company': {'required': True},
        }

# class UserListDocumentSerializer(DocumentSerializer):
#     class Meta:
#         document = UserDocument
#         fields = ('first_name', 'last_name', 'phone')
