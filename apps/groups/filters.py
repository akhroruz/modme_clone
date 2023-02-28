from django_filters import FilterSet, ModelMultipleChoiceFilter
from django_filters.rest_framework import DjangoFilterBackend
from django_filters.utils import translate_validation
from rest_framework.exceptions import ValidationError

from groups.models import Group, Branch, Course
from users.models import User


class CustomGroupDjangoFilterBackend(DjangoFilterBackend):

    def filter_queryset(self, request, queryset, view):

        filter_set = self.get_filterset(request, queryset, view)
        query_params = request.query_params
        if not query_params.get('branch'):
            raise ValidationError({'success': False, 'error': {'branch': ['The branch id field is required.']}})

        if filter_set is None:
            return queryset

        if not filter_set.is_valid() and self.raise_exception:
            raise translate_validation(filter_set.errors)
        return filter_set.qs


class CustomCompanyDjangoFilterBackend(DjangoFilterBackend):

    def filter_queryset(self, request, queryset, view):

        filter_set = self.get_filterset(request, queryset, view)
        query_params = request.query_params
        if not query_params.get('company'):
            raise ValidationError({'success': False, 'error': {'company': ['The company field is required.']}})

        if filter_set is None:
            return queryset

        if not filter_set.is_valid() and self.raise_exception:
            raise translate_validation(filter_set.errors)
        return filter_set.qs


class GroupFilter(FilterSet):
    courses = ModelMultipleChoiceFilter(field_name='course', queryset=Course.objects.all())
    teacher = ModelMultipleChoiceFilter(field_name='teacher__first_name', queryset=User.objects.all(),
                                        to_field_name='name')
    branch = ModelMultipleChoiceFilter(queryset=Branch.objects.all())
    days = ModelMultipleChoiceFilter(field_name='days', queryset=Group.objects.all())

    class Meta:
        model = Group
        fields = ('branch', 'status', 'teacher', 'courses', 'days', 'start_date', 'end_date')
