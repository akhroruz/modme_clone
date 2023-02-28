from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField
from rest_framework.serializers import ModelSerializer

from users.models import User, Blog


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
