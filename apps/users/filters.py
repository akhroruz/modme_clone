from django.contrib.auth.models import Group
from django_filters import ModelMultipleChoiceFilter
from django_filters.rest_framework import FilterSet, DjangoFilterBackend
from django_filters.utils import translate_validation
from rest_framework.exceptions import ValidationError

from groups.models import Branch
from users.models import User


class UserFilter(FilterSet):
    groups = ModelMultipleChoiceFilter(field_name='full_name', queryset=User.objects.all())
    user_type = ModelMultipleChoiceFilter(field_name='role__name', queryset=Group.objects.all(), to_field_name='name')
    branch = ModelMultipleChoiceFilter(queryset=Branch.objects.all())

    class Meta:
        model = User
        fields = ['groups', 'first_name', 'last_name', 'phone', 'user_type', 'branch']

    # filter_overrides = {
    #     ArrayField: {
    #         'filter_class': CharFilter,
    #         'extra': lambda f: {
    #             'lookup_expr': 'icontains',
    #         },
    #     },
    # }


class CustomUserDjangoFilterBackend(DjangoFilterBackend):

    def filter_queryset(self, request, queryset, view):

        filter_set = self.get_filterset(request, queryset, view)
        query_params = request.query_params
        if not query_params.get('branch') and not query_params.get('user_type'):
            raise ValidationError(
                {'success': False, 'error': {'branch': ['The branch id field is required.'],
                                             'user_type': ['The user type field is required.']}}
            )

        if not query_params.get('branch'):
            raise ValidationError({'success': False, 'error': {'branch': ['The branch id field is required.']}})
        if not query_params.get('user_type'):
            raise ValidationError({'success': False, 'error': {'user_type': ['The user type field is required.']}})

        if filter_set is None:
            return queryset

        if not filter_set.is_valid() and self.raise_exception:
            raise translate_validation(filter_set.errors)
        return filter_set.qs
