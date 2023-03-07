from rest_framework.serializers import ModelSerializer

from users.models import User, ArchivedUser


class ArchiveUserListModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name')


class ArchiveUserCreateModelSerializer(ModelSerializer):
    class Meta:
        model = ArchivedUser
        fields = '__all__'

    def create(self, validated_data):
        return super().create(validated_data)
