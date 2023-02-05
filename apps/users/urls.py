from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import ArchiveReasonsModelViewSet, UserModelViewSet, LeadIncrementModelViewSet, LeadModelViewSet, \
    UpdateProfileView, BlogModelViewSet

router = DefaultRouter()
router.register('user', UserModelViewSet, basename='user')
router.register('archive-reasons', ArchiveReasonsModelViewSet, basename='archive_reasons')
router.register('lead', LeadModelViewSet, basename='lead')
router.register('lead-increment', LeadIncrementModelViewSet, basename='lead_increment')
router.register('news-blog', BlogModelViewSet, basename='news_blog')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token', TokenObtainPairView.as_view(), name='get_token'),
    path('auth/refresh-token', TokenRefreshView.as_view(), name='refresh_token'),
    path('auth/change_profile/<int:pk>', UpdateProfileView.as_view(), name='change_profile'),
]
