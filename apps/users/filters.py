from django.contrib.auth.models import Group
from django_filters import ModelMultipleChoiceFilter
from django_filters.rest_framework import FilterSet
from users.models import User


class UserFilter(FilterSet):
    groups = ModelMultipleChoiceFilter(field_name='full_name', queryset=User.objects.all())
    role = ModelMultipleChoiceFilter(field_name='role__name', queryset=Group.objects.all(), to_field_name='name')

    class Meta:
        model = User
        fields = ['groups', 'first_name', 'last_name', 'phone', 'role']
