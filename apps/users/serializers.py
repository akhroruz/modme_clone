from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, CharField, ValidationError

from apps.users.models import User


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
    phone = serializers.IntegerField(required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'password', 'confirm_password')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    # TODO
    # SHOULD WRITE VALIDATE FOR PHONE
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone=validated_data['phone']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user


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

        return result



class StudentModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['phone', 'full_name', 'birth', 'gender', 'comment', 'datas', 'balance']
        extra_kwargs = {
            'birth': {'required': False}, 'datas': {'required': False},
            'full_name': {'required': True},
            'phone': {'required': True}, }
