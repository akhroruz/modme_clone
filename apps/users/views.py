from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

import users.urls
from apps.users.models import User
from apps.users.serializers import StudentModelSerializer, UserModelSerializer, RegisterSerializer
from users.pagination import StudentPagination


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
    lookup_url_kwarg = 'id'
    parser_classes = (MultiPartParser, FormParser,)
    pagination_class = StudentPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'full_name', 'phone']
    ordering = ['full_name']
