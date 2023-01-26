from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet

from apps.users.models import User
from apps.users.serializers import UserModelSerializer


class UserModelViewSet(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    parser_classes = (MultiPartParser,)
