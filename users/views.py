from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserModelSerializer


class UserModelViewSet(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
