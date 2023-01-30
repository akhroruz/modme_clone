from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from apps.users.models import User
from apps.users.serializers import RegisterSerializer
from apps.users.serializers import UserModelSerializer
from users.pagination import StudentPagination
from users.serializers import StudentModelSerializer


class UserModelViewSet(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    parser_classes = (MultiPartParser,)


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
    lookup_url_kwarg = 'uuid'


class StudentModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = StudentModelSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = 'uuid'
    parser_classes = (MultiPartParser, FormParser,)
    pagination_class = StudentPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['full_name', 'phone']

    def get_permissions(self):
        if self.action in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()
