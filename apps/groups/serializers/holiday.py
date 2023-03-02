from rest_framework.serializers import ModelSerializer
from groups.models import Holiday


class HolidayListModelSerializer(ModelSerializer):
    class Meta:
        model = Holiday
        fields = 'id', 'holiday_date', 'branch', 'affect_payment', 'name', 'created_at'


class HolidayCreateModelSerializer(ModelSerializer):
    class Meta:
        model = Holiday
        fields = 'holiday_date', 'branch', 'name'
