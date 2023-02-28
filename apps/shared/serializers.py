from rest_framework.settings import api_settings
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):  # noqa
    def validate(self, attrs):
        data = super().validate(attrs)
        data['token_type'] = 'bearer'
        data['expires_in'] = api_settings.ACCESS_TOKEN_LIFETIME
        return data
