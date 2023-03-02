from django.contrib.auth.models import Group as Role
from rest_framework.serializers import ModelSerializer
from groups.models import Course, Company


class CompanyModelSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class HomeModelSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class RoleModelSerializer(ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'
