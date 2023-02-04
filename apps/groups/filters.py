# from rest_framework import generics
# from django_filters import rest_framework as filters
#
# from groups.models import Branch
#
#
# class BranchFilter(filters.FilterSet):
#     branch = filters.NumberFilter(field_name="price", lookup_expr='gte')
#     max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
#
#     class Meta:
#         model = Branch
#         fields = ['id']
