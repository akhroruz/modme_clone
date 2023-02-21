from django.urls import path, include
from rest_framework.routers import DefaultRouter

from groups.views import GroupModelViewSet, BranchModelViewSet, RoomModelViewSet, HomeListAPIView
from groups.views.views import CompanyModelViewSet

router = DefaultRouter()
router.register('group', GroupModelViewSet, basename='group')
router.register('branch', BranchModelViewSet, basename='branch')
router.register('room', RoomModelViewSet, basename='room')
router.register('company', CompanyModelViewSet, basename='company')

urlpatterns = [
    path('home', HomeListAPIView.as_view(), name='home'),
    path('', include(router.urls)),
]
