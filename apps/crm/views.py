from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from users.models import User


# Reports API
# https://api.modme.dev/v1/reports/conversion/teachers?branch_ids[]=189&branch_ids[]=147&date_from=2023-01-02&date_to=2023-03-02

class TeacherReportModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    filter_backends = DjangoFilterBackend

# https://api.modme.dev/v1/reports/students/activity?branch_ids[]=189&date_from=2023-01-02&date_to=2023-03-02
# https://api.modme.dev/v1/reports/conversion/courses?branch_ids[]=189&date_from=2023-01-02&date_to=2023-03-02
# https://api.modme.dev/v1/conversion?branch_id=189&from=2023-03-01&to=2023-03-02
