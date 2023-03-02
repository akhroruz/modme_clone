from rest_framework.serializers import ModelSerializer

from users.models import User


class ArchiveUserListModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name')

    # def to_representation(self, instance: Archive):
    #     rep = super().to_representation(instance)
    #     rep['users'] = ArchiveUserListModelSerializer(User.objects.filter(is_archive=True), many=True).data
    #     return rep

