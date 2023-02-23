from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import ArchiveReasonsModelViewSet, UserModelViewSet, LeadIncrementModelViewSet, LeadModelViewSet, \
    UpdateProfileView, BlogModelViewSet

router = DefaultRouter()
router.register('user', UserModelViewSet, 'user')
# router.register('user-search', UserDocumentView, 'user_search')
router.register('archive-reasons', ArchiveReasonsModelViewSet, 'archive_reasons')
router.register('lead', LeadModelViewSet, 'lead')
router.register('lead-increment', LeadIncrementModelViewSet, 'lead_increment')
router.register('news-blog', BlogModelViewSet, 'news_blog')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token', TokenObtainPairView.as_view(), name='get_token'),
    path('auth/refresh-token', TokenRefreshView.as_view(), name='refresh_token'),
    path('auth/change-profile/<int:pk>', UpdateProfileView.as_view(), name='change_profile'),
]
