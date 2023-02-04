from rest_framework.generics import ListAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions
from rest_framework.viewsets import ModelViewSet

from groups.models import Branch, Room, Course, Company
from groups.serializers import BranchModelSerializer, \
    RoomListModelSerializer, RoomCreateModelSerializer, HomeModelSerializer, CompanyModelSerializer
from shared.permissions import IsAdministrator


class BranchModelViewSet(ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchModelSerializer
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = BranchFilter
    parser_classes = (MultiPartParser,)
    # permission_classes = (IsAuthenticated & CustomDjangoObjectPermissions, )
    # permission_classes = [IsWriteUser]
    # permission_classes_per_method = {
    #     except for list and retrieve where both users with "write" or "read-only"
    #     permissions can access the endpoints.
        # "list": [IsWriteUser | IsReadOnlyUser],
        # "retrieve": [IsWriteUser | IsReadOnlyUser]
    # }
    # def get_queryset(self):
    #     return Branch.objects.all()
        # return self.request.user.branch.all()


class RoomModelViewSet(ModelViewSet):
    serializer_class = RoomCreateModelSerializer
    queryset = Room.objects.all()
    permission_classes = IsAuthenticated, DjangoObjectPermissions, IsAdministrator

    def get_serializer_class(self):
        if self.action == 'list':
            return RoomListModelSerializer
        return super().get_serializer_class()


class HomeListAPIView(ListAPIView):
    queryset = Course.objects.all()
    serializer_class = HomeModelSerializer


class CompanyModelViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanyModelSerializer
    permission_classes = IsAuthenticated, DjangoObjectPermissions, IsAdministrator
