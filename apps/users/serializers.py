from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.fields import ListField, IntegerField
from rest_framework.relations import SlugRelatedField
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer, CharField, ValidationError

from groups.models import CourseGroup, Branch
from users.models import User, Comment, LeadIncrement, Lead, Archive


class LidModelSerializer(ModelSerializer):
    class Meta:
        model = Lead
        fields = ('phone', 'full_name', 'comment', 'lid_increment')


class LidIncrementModelSerializer(ModelSerializer):
    class Meta:
        model = LeadIncrement
        fields = ('name',)


class UserBranchListModelSerializer(ModelSerializer):
    class Meta:
        model = Branch
        fields = ('id', 'name')


class UserGroupListModelSerializer(ModelSerializer):
    class Meta:
        model = CourseGroup
        fields = ('id', 'name')

    def to_representation(self, instance: CourseGroup):
        rep = super().to_representation(instance)
        rep['branches'] = UserBranchListModelSerializer(instance.branch, many=True).data
        return rep


class UserListCommentModelSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text')


class UserListModelSerializer(ModelSerializer):
    role = SlugRelatedField(many=True, read_only=True, slug_field='name')

    class Meta:
        model = User
        fields = (
            'id', 'full_name', 'gender', 'birth_date', 'phone', 'photo', 'balance', 'deleted_at', 'data', 'role',
            'is_archive'
        )

    def to_representation(self, instance: User):
        rep = super().to_representation(instance)
        rep['groups'] = UserGroupListModelSerializer(instance.coursegroup_set.all(), many=True).data
        rep['comments'] = UserListCommentModelSerializer(instance.comment, many=True).data
        return rep


class ArchiveUserListModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ArchiveListModelSerializer(ModelSerializer):
    class Meta:
        model = Archive
        fields = '__all__'

    def to_representation(self, instance: Archive):
        rep = super().to_representation(instance)
        rep['users'] = User.objects.filter(is_archive=True)
        return rep


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


# class RegisterSerializer(ModelSerializer):
#     phone = IntegerField(required=True)
#     password = CharField(write_only=True, required=True, validators=[validate_password])
#     confirm_password = CharField(write_only=True, required=True)
#
#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'phone', 'password', 'confirm_password')
#         extra_kwargs = {
#             'first_name': {'required': True},
#             'last_name': {'required': True}
#         }
#
#     def validate(self, attrs):
#         if attrs['password'] != attrs['confirm_password']:
#             raise ValidationError({"password": "Password fields didn't match."})
#         return attrs
#
#     def create(self, validated_data):
#         user = User.objects.create(
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'],
#             phone=validated_data['phone']
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = CharField(write_only=True, required=True)
    new_password = CharField(write_only=True, required=True, validators=[validate_password])
    new_confirm_password = CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'new_confirm_password')

    def validate(self, obj):
        if obj['new_password'] != obj['new_confirm_password']:
            raise ValidationError({'new_password': "Password fields didn't match"})
        return obj

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise ValidationError({'old_password': "Old password is not correct"})

        return value

    def update(self, result, validated_data):
        result.set_password(validated_data['new_password'])
        result.save()
        return Response({'successfully updated password'})


'''
name
phone
role
birthday date
gender
photo
password

'''


class UpdateProfileSerializer(ModelSerializer):
    phone = IntegerField(required=True)

    class Meta:
        fields = ('first_name', 'phone', 'role', 'birth_date', 'gender', 'photo', 'password')
        model = User

    def validate_phone(self, phone):
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
