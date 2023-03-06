from rest_framework.serializers import ModelSerializer

from users.models import User


class ArchiveUserListModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name')
