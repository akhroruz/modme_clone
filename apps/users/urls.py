from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserModelViewSet, LidIncrementModelViewSet, LidModelViewSet

router = DefaultRouter()
router.register('auth/user', UserModelViewSet, basename='user')
router.register('lid', LidModelViewSet, basename='lid')
router.register('lid-increment', LidIncrementModelViewSet, basename='lid_increment')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token', TokenObtainPairView.as_view(), name='get_token'),
    path('auth/refresh-token', TokenRefreshView.as_view(), name='refresh_token'),
]
