from django_filters import ModelMultipleChoiceFilter
from django_filters.rest_framework import FilterSet

from users.models import User


class UserFilter(FilterSet):
    groups = ModelMultipleChoiceFilter(field_name='full_name', conjoined=True, queryset=User.objects.all())

    class Meta:
        model = User
        fields = ['groups']
