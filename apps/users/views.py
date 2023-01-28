from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.viewsets import ModelViewSet
from apps.users.serializers import UserModelSerializer

from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
# from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from apps.users.models import User


class UserModelViewSet(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    parser_classes = (MultiPartParser,)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
