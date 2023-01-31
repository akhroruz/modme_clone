from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

import users.urls
from apps.users.models import User
from users.pagination import StudentPagination
from users.serializers import StudentModelSerializer
from apps.users.serializers import RegisterSerializer, UserModelSerializer, ChangePasswordSerializer


class UserModelViewSet(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    parser_classes = (MultiPartParser,)


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer


class StudentModelViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = StudentModelSerializer
    permission_classes = [AllowAny]
    lookup_url_kwarg = 'id'
    parser_classes = (MultiPartParser, FormParser,)
    pagination_class = StudentPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['phone']
