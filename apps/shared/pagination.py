from rest_framework.pagination import PageNumberPagination


class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'per_page'
    page_size_query_description = 'Number of pages to'
