from django.contrib.auth.models import Group
from django_filters import ModelMultipleChoiceFilter
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from django_filters.utils import translate_validation
from rest_framework.exceptions import ValidationError

from groups.models import Branch
from users.models import User


class UserFilter(FilterSet):
    groups = ModelMultipleChoiceFilter(field_name='full_name', queryset=User.objects.all())
    role = ModelMultipleChoiceFilter(field_name='role__name', queryset=Group.objects.all(), to_field_name='name')
    branch = ModelMultipleChoiceFilter(queryset=Branch.objects.all())

    class Meta:
        model = User
        fields = ['groups', 'first_name', 'last_name', 'phone', 'role', 'branch']
 # filter_overrides = {
        #     ArrayField: {
        #         'filter_class': CharFilter,
        #         'extra': lambda f: {
        #             'lookup_expr': 'icontains',
        #         },
        #     },
        # }


class CustomDjangoFilterBackend(DjangoFilterBackend):

    def filter_queryset(self, request, queryset, view):

        filterset = self.get_filterset(request, queryset, view)
        if not request.query_params.get('branch'):
            raise ValidationError('Branch is required')

        if filterset is None:
            return queryset

        if not filterset.is_valid() and self.raise_exception:
            raise translate_validation(filterset.errors)
        return filterset.qs