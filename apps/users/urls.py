from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import ArchiveReasonsModelViewSet, UserModelViewSet, LeadIncrementModelViewSet, LeadModelViewSet, \
    UpdateProfileView

router = DefaultRouter()
router.register('user', UserModelViewSet, basename='user')
router.register('lid', LeadModelViewSet, basename='lid')
router.register('lid-increment', LeadIncrementModelViewSet, basename='lid_increment')
router.register('archiveReasons', ArchiveReasonsModelViewSet, basename='archive_categories')
router.register('auth/user', UserModelViewSet, basename='user')
router.register('lead', LeadModelViewSet, basename='lead')
router.register('lead-increment', LeadIncrementModelViewSet, basename='lead_increment')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token', TokenObtainPairView.as_view(), name='get_token'),
    path('auth/refresh-token', TokenRefreshView.as_view(), name='refresh_token'),
    path('auth/change_profile/<int:pk>', UpdateProfileView.as_view(), name='change_profile'),
]
