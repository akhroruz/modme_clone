from django.contrib.auth.models import Group as Role
from rest_framework.serializers import ModelSerializer

from groups.models import Course, Holiday, Company


class CompanyModelSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class HomeModelSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class HolidayListModelSerializer(ModelSerializer):
    class Meta:
        model = Holiday
        fields = 'name', 'holiday_date', 'affect_payment', 'branch', 'created_at'


class HolidayCreateModelSerializer(ModelSerializer):
    class Meta:
        model = Holiday
        fields = 'name', 'holiday_date', 'affect_payment'


class RoleModelSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class CourseModelSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'
