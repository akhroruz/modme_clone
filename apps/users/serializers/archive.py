from rest_framework.serializers import ModelSerializer

from users.models import User, Archive


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
