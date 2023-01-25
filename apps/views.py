from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from apps.models import Role, Branch
from apps.serializers import RoleModelSerializer, BranchModelSerializer


class RoleModelViewSet(ModelViewSet):
    serializer_class = RoleModelSerializer
    queryset = Role.objects.all()


class BranchModelViewSet(ModelViewSet):
    serializer_class = BranchModelSerializer
    queryset = Branch.objects.all()
