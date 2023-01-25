from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserModelViewSet

router = DefaultRouter()
router.register('user', UserModelViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('token', TokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh', TokenRefreshView.as_view(), name='refresh_token'),
]
