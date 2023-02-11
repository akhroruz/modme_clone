from rest_framework import filters


class MultipleFilterBackend(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        filter_field = request.query_params.getlist('role')
        if filter_field:
            return queryset.filter(role__name__in=filter_field)
        return queryset

# class MyFilterSet(django_filters.FilterSet):
#     name = django_filters.CharFilter(lookup_expr='icontains')
#     date = django_filters.DateFilter()
#
#
# class MultipleChoiceFilter(BaseFilterBackend):
#     def filter_queryset(self, request, queryset, view):
#         multiple_choices = request.query_params.getlist('role_name')
#         if multiple_choices:
#             queryset = queryset.filter(role__name__in=multiple_choices)
#         return queryset
