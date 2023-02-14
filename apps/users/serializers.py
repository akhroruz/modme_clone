from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from rest_framework.fields import ListField, IntegerField, SerializerMethodField
from rest_framework.serializers import ModelSerializer, CharField, ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from groups.models import Branch
from users.documents import UserDocument
from users.models import User, Comment, LeadIncrement, Lead, Archive, Blog


class LeadModelSerializer(ModelSerializer):
    class Meta:
        model = Lead
        fields = ('phone', 'full_name', 'comment', 'lead_increment', 'status')


class LeadIncrementModelSerializer(ModelSerializer):
    class Meta:
        model = LeadIncrement
        fields = ('name',)


class UserBranchListModelSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = ('id', 'name')


class UserGroupListModelSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class UserListCommentModelSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text')


class UserListModelSerializer(ModelSerializer):
    role = SerializerMethodField('get_roles')

    def get_roles(self, obj: User):  # noqa
        return obj.role.values('id', 'name')

    class Meta:
        model = User
        fields = (
            'id', 'full_name', 'gender', 'birth_date', 'phone', 'photo', 'balance', 'deleted_at', 'data', 'role',
            'is_archive'
        )

    def to_representation(self, instance: User):
        rep = super().to_representation(instance)

        if user_type := self.context['request'].query_params.get('user_type'):
            if user_type == 'teacher':
                rep['groups'] = UserGroupListModelSerializer(instance.group_set.all(), many=True).data
            elif user_type == 'student':
                rep['groups'] = UserGroupListModelSerializer(instance.groups.all(), many=True).data
        rep['branches'] = UserBranchListModelSerializer(instance.branch, many=True).data
        return rep


class ArchiveUserListModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name')


class ArchiveListModelSerializer(ModelSerializer):
    class Meta:
        model = Archive
        fields = '__all__'

    def to_representation(self, instance: Archive):
        rep = super().to_representation(instance)
        rep['users'] = ArchiveUserListModelSerializer(User.objects.filter(is_archive=True), many=True).data
        return rep


class ArchiveCreateModelSerializer(ModelSerializer):
    class Meta:
        model = Archive
        fields = ('id', 'gender', 'birth_date', 'phone', 'photo', 'balance', 'datas')


class UserCreateRoleModelSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserCreateModelSerializer(ModelSerializer):
    role = ListField(write_only=True)
    password = CharField(write_only=True)

    class Meta:
        model = User
        fields = ('phone', 'first_name', 'gender', 'birth_date', 'photo', 'comment', 'data', 'role', 'password')

    def create(self, validated_data):
        validated_data['role'] = Group.objects.filter(name__in=validated_data['role'][0].split(','))
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


class UpdateProfileSerializer(ModelSerializer):
    phone = IntegerField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'phone', 'role', 'birth_date', 'gender', 'photo', 'password')

    def validate_phone(self, phone):  # noqa
        user = User.objects.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(phone=phone).exists():
            raise ValidationError({'phone': "This phone is already in use."})
        return phone

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise ValidationError({'authorize': "You dont have permission for this user."})
        instance.set_password(validated_data['password'])

        instance.first_name = validated_data['first_name']
        instance.phone = validated_data['phone']
        instance.role = validated_data['role']
        instance.birth_date = validated_data['birth_date']
        instance.gender = validated_data['gender']
        instance.photo = validated_data['photo']
        instance.password = validated_data['password']
        instance.save()
        return instance


class BlogModelSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = ('title', 'text', 'public', 'visible_all', 'view_count')
        extra_kwargs = {
            'created_by': {'required': False},
            'updated_by': {'required': False},
            'view_count': {'required': False},
        }


class UserListDocumentSerializer(DocumentSerializer):
    class Meta:
        document = UserDocument
        fields = ('first_name', 'last_name', 'phone')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):  # noqa
    def validate(self, attrs):
        data = super().validate(attrs)
        data['token_type'] = 'bearer'
        data['expires_in'] = api_settings.ACCESS_TOKEN_LIFETIME
        return data
