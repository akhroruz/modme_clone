from django.urls import path, include
from rest_framework.routers import DefaultRouter

from groups.views import GroupModelViewSet, BranchModelViewSet, RoomModelViewSet, HomeListAPIView

router = DefaultRouter()
router.register('group', GroupModelViewSet, basename='group')
router.register('branch', BranchModelViewSet, basename='branch')
router.register('room', RoomModelViewSet, basename='room')

urlpatterns = [
    path('home', HomeListAPIView.as_view(), name='home'),
    path('', include(router.urls)),
]
