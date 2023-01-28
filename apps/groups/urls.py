from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.viewsets import ModelViewSet

from apps.groups.views import RoleModelViewSet, BranchModelViewSet, RoomModelViewSet, CourseModelViewSet, \
    WeekendModelViewSet

router = DefaultRouter()
# router.register('role', RoleModelViewSet, basename='role')
router.register('branch', BranchModelViewSet, basename='branch')
router.register('room', RoomModelViewSet, basename='room')
router.register('course', CourseModelViewSet, basename='course')
# router.register('weekend', WeekendModelViewSet, basename='weekend')
# router.register('group', GroupModelViewSet, basename='group')

urlpatterns = [
    path('', include(router.urls)),
]
