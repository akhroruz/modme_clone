from rest_framework.serializers import ModelSerializer

from groups.models import Room


class RoomCreateModelSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class RoomListModelSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = 'id', 'name'
