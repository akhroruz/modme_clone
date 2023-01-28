from knox import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.users.views import UserModelViewSet

router = DefaultRouter()
# router.register('user', UserModelViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/token', TokenObtainPairView.as_view(), name='get_token'),
    path('auth/refresh-token', TokenRefreshView.as_view(), name='refresh_token'),
]
